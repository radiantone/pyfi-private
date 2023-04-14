"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
# logging.basicConfig(level=logging.DEBUG)
import configparser
import datetime
import gc
import logging
import multiprocessing
import os
import platform
import shutil
import signal
from multiprocessing import Condition
from pathlib import Path
from typing import Any, List, Tuple

import psutil
from flask import Flask
from sqlalchemy import inspect

from pyfi.blueprints.show import blueprint
from pyfi.db import get_session
from pyfi.db.model import (
    AgentModel,
    DeploymentModel,
    NodeModel,
    ProcessorModel,
    WorkerModel,
)
from pyfi.worker import WorkerService

logger = logging.getLogger(__name__)

lock = Condition()

app = Flask(__name__)

app.register_blueprint(blueprint)

HOME = str(Path.home())

CONFIG = configparser.ConfigParser()

global HOSTNAME
HOSTNAME = platform.node()

CPUS = multiprocessing.cpu_count()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]

HOME = str(Path.home())
ini = HOME + "/pyfi.ini"
if os.path.exists(ini):
    CONFIG.read(ini)


@app.route("/")
def health():
    import json

    return json.dumps({"status": "green"})


def import_class(name):
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def kill_containers():
    """Kill running containers"""
    import docker

    if "AGENT_CWD" in os.environ:
        agent_cwd = os.environ["AGENT_CWD"]

        if os.path.exists(f"{agent_cwd}/containers.pid"):
            client = docker.from_env()
            logger.debug("Found containers.pid")
            with open(f"{agent_cwd}/containers.pid", "r") as cfile:
                pids = cfile.readlines()
                for pid in pids:
                    try:
                        logger.info("Getting client container %s", pid)
                        container = client.containers.get(pid.strip())
                        logger.info("Killing container...")
                        container.kill()
                        logger.info("Done")
                    except Exception as ex:
                        logging.error("Error obtaining or killing container %s", pid)

            try:
                os.remove(f"{agent_cwd}/containers.pid")
            except Exception:
                pass


class AgentPlugin:
    pass


class AgentService:
    dburi: str = "postgresql://postgres:postgres@" + HOSTNAME + ":5432/pyfi"
    port: int = 8003
    config = None
    clean: bool = False
    user = None
    name: str
    pool: int = 4
    cpus: int = -1
    backend: str = "redis://localhost"
    broker: str = "pyamqp://localhost"
    size: int = 10
    plugins: List[AgentPlugin] = []
    workerport: int = 8020


class AgentWebServerPlugin(AgentPlugin):
    """Health check web endpoint"""

    def __init__(self):
        self.process = None
        logger.debug("[AgentWebServerPlugin] Creating")

    def start(self, agent: AgentService, **kwargs):

        logger.debug("[AgentWebServerPlugin] Starting")
        import gunicorn.app.base
        from billiard.context import Process

        cpus = multiprocessing.cpu_count()

        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                config = {
                    key: value
                    for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None
                }
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        #########################################################################
        # Agent endpoints & health checks
        #########################################################################
        def web_server():
            from setproctitle import setproctitle

            try:
                setproctitle("pyfi agent::web_server")
                logger.info(
                    "[AgentWebServerPlugin] Starting web server on %s", agent.port
                )
                logger.debug("[AgentWebServerPlugin] Startup Complete")
                # bjoern.run(app, "0.0.0.0", agent.port)
                options = {
                    "bind": "%s:%s" % ("0.0.0.0", str(agent.port)),
                    "workers": cpus,
                    # 'threads': number_of_workers(),
                    "timeout": 120,
                }
                StandaloneApplication(app, options).run()
            except Exception as ex:
                logging.error(ex)
                logger.info("web_server: exiting...")

        self.process = webserver = Process(target=web_server, daemon=True)
        webserver.start()

    def wait(self):
        return self.process.join()


# noinspection PyUnusedLocal
class AgentShutdownPlugin(AgentPlugin):
    """Detect signal and gracefully shutown"""

    def __init__(self):
        logger.debug("[AgentShutdownPlugin] Creating")

    def start(self, agent_service: AgentService, **kwargs):
        logger.debug("[AgentShutdownPlugin] Starting")

        def shutdown(*args):
            """Shutdown worker"""
            from psutil import Process

            kill_containers()
            logger.info("Shutting down agent...")
            process = Process(os.getpid())

            logger.info("    Terminating child processes...")
            for child in process.children(recursive=True):
                logger.info(
                    "         Process pid {}: Killing child {}".format(
                        process.pid, child.pid
                    )
                )
                try:
                    child.kill()
                except:
                    """We can ignore exceptions here"""
                    pass

            logger.info("CWD is %s %s", os.getcwd(), os.environ["AGENT_CWD"])

            agent_cwd = os.environ["AGENT_CWD"]

            logger.info("Killing workers")

            if os.path.exists(f"{agent_cwd}/agent.pid"):
                os.remove(f"{agent_cwd}/agent.pid")

            if os.path.exists(f"{agent_cwd}/worker.pid"):
                with open(f"{agent_cwd}/worker.pid", "r") as wfile:
                    workerpids = wfile.readlines()

                    for workerpid in workerpids:
                        workerpid = int(workerpid)
                        logger.info("Killing worker process %s", workerpid)
                        try:
                            os.killpg(os.getpgid(workerpid), 15)
                            os.kill(workerpid, signal.SIGKILL)
                        except Exception as ex:
                            logging.warning(ex)

                os.remove(f"{agent_cwd}/worker.pid")

                os.killpg(os.getpgid(os.getpid()), 15)
                os.kill(os.getpid(), signal.SIGKILL)
                process.kill()
                process.terminate()
            exit(0)

        signal.signal(signal.SIGINT, shutdown)

        logger.debug("[AgentShutdownPlugin] Startup Complete")

    def wait(self):
        pass


class AgentMonitorPlugin(AgentPlugin):
    """Check if agent is killed and update node resource stats"""

    def __init__(self, *args, **kwargs):
        self.process = None
        self.port = None
        self.workerclass = None
        self.kwargs = None
        self.workerproc = None
        import sched
        import time

        self.monitors = {}

        logger.debug("[AgentMonitorPlugin] Creating")
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.processors = []
        self.agent_service = None
        self.workers = []
        self.basedir = os.getcwd()

    def deployment_monitor(self, agent):

        with get_session() as session:
            logger.debug("[DeploymentMonitor] Getting deployments %s", agent.hostname)

            """ Get deployments for this agent """
            mydeployments = (
                session.query(DeploymentModel).filter_by(hostname=agent.hostname).all()
            )

            """ Check for any killed workers """
            for mydeployment in mydeployments:
                if not mydeployment.worker:
                    continue
                myworker = mydeployment.worker

                if myworker.requested_status == "kill":
                    logging.debug("Killing worker process %s", myworker.process)
                    try:
                        os.kill(myworker.process, signal.SIGTERM)
                    except:
                        pass
                    myworker.requested_status = "restart"
                    session.commit()

            """ Monitor deployments """
            for mydeployment in mydeployments:

                logger.debug(
                    "Got deployment %s worker %s",
                    mydeployment.name,
                    mydeployment.worker.name if mydeployment.worker else None,
                )

                try:
                    session.refresh(mydeployment)
                    logging.debug("Refreshing deployment %s", mydeployment.name)
                except:
                    try:
                        session.merge(mydeployment)
                        logging.debug("Merged deployment %s", mydeployment.name)
                    except:
                        session.add(mydeployment)
                        logging.debug("Add deployment %s", mydeployment.name)

                try:
                    logging.debug("Deployment Processor %s", mydeployment.processor)

                    """ If one of my processors is in the move state, then ignore it """
                    if mydeployment.processor.requested_status == "move":
                        continue

                    found = False
                    """ Update my list of processors with the deployment.processor """
                    for processor in self.processors:

                        if processor["id"] == mydeployment.processor.id:
                            found = True

                            """ If this deployment is requesting update then kill the worker for it """
                            if mydeployment.requested_status == "update":
                                logging.debug(
                                    "Deployment %s has changed for processor %s",
                                    mydeployment,
                                    mydeployment.processor,
                                )
                                logging.debug("Updating deployment %s", mydeployment)
                                mydeployment.status = "updating"
                                session.commit()
                                # Restart the worker, which will pull the assigned deployment
                                # from database and restart with new configs
                                logging.debug("Killing worker")
                                processor["worker"]["process"].kill()
                                processor["worker"] = None
                                mydeployment.requested_status = "ready"
                                mydeployment.status = "updating"
                                session.commit()

                    """ If I don't already manage the processor for this deployment in my list. """
                    if not found:
                        """Add a new processor object to my list"""
                        self.processors += [
                            {
                                "worker": None,
                                "id": mydeployment.processor.id,
                            }
                        ]
                        logging.debug("Added processor %s", mydeployment.processor)

                    """ Now look at all my processors in my list and create workers if necessary """
                    for processor in self.processors:
                        """Retrieve my processor from database for this reference"""
                        myprocessor = (
                            session.query(ProcessorModel)
                            .filter_by(id=processor["id"])
                            .first()
                        )

                        logging.debug(
                            "Processor.requested_status START %s %s",
                            myprocessor.requested_status,
                            myprocessor,
                        )

                        process_died = False

                        """ Processor can be in one of many states """

                        if myprocessor.requested_status == "removed":
                            if processor["worker"] is not None:
                                logging.debug("Killing worker")
                                try:
                                    processor["worker"]["process"].kill()
                                    processor["worker"] = None
                                    logging.debug("Killed worker")
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["delete"] = True

                            if os.path.exists("work/" + myprocessor.id):
                                logging.debug(
                                    "Removing work directory %s",
                                    "work/" + myprocessor,
                                )
                                shutil.rmtree("work/" + myprocessor.id)

                            logging.debug("Processor is removed")

                            continue

                        if myprocessor.requested_status == "restart":
                            if processor["worker"] is not None:
                                logging.debug("Killing worker")
                                try:

                                    processor["worker"]["process"].kill()
                                    processor["worker"] = None
                                    logging.debug("Killed worker")
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            myprocessor.requested_status = "start"
                            myprocessor.status = "stopped"
                            mydeployment.worker.status = "stopped"
                            mydeployment.worker.requested_status = "ready"
                            processor["status"] = "stopped"

                            logging.debug("Processor is stopped")

                            session.add(mydeployment.worker)
                            session.add(myprocessor)

                        if myprocessor.requested_status == "paused":
                            if processor["worker"] is not None:
                                logging.debug("Pausing worker")
                                try:
                                    processor["worker"]["process"].suspend()
                                    logging.debug("Paused worker")
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            myprocessor.requested_status = "ready"
                            myprocessor.status = "paused"
                            mydeployment.worker.status = "paused"
                            mydeployment.worker.requested_status = "ready"

                            logging.debug("Processor is paused")

                            session.add(mydeployment.worker)
                            session.add(myprocessor)

                            continue

                        if myprocessor.requested_status == "resumed":
                            if processor["worker"] is not None:
                                logging.debug("Resuming worker")
                                try:
                                    processor["worker"]["process"].resume()
                                    logging.debug("Paused worker")
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            myprocessor.requested_status = "ready"
                            myprocessor.status = "resumed"
                            mydeployment.worker.status = "resumed"
                            mydeployment.worker.requested_status = "ready"

                            logging.debug("Processor is resumed")

                            session.add(mydeployment.worker)
                            session.add(myprocessor)

                            continue

                        if myprocessor.requested_status == "stopped":
                            if processor["worker"] is not None:
                                logging.debug("Killing worker")
                                try:
                                    processor["worker"]["process"].kill()
                                    processor["worker"] = None
                                    logging.debug("Killed worker")
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            myprocessor.requested_status = "ready"
                            myprocessor.status = "stopped"
                            mydeployment.worker.status = "stopped"
                            mydeployment.worker.requested_status = "ready"

                            logging.debug("Processor is stopped")

                            session.add(mydeployment.worker)
                            session.add(myprocessor)

                        if myprocessor.requested_status == "started":
                            if processor["worker"] is None:
                                # Spin up worker if I have CPU's available
                                # Create a worker, link it to the processor
                                # Add it to workers list
                                pass

                        """ If we have a worker process, poll it to see if its still alive  """
                        if "worker" in processor:
                            try:
                                logging.info(
                                    "Processor.requested_status 0 %s",
                                    myprocessor.requested_status,
                                )
                                if (
                                    processor["worker"]
                                    and processor["worker"]["wprocess"]
                                ):
                                    process_died = (
                                        processor["worker"]["wprocess"].poll()
                                        is not None
                                    )
                                    logging.info(
                                        "PROCESS_DIED is %s for %s",
                                        process_died,
                                        processor["worker"],
                                    )
                            except:
                                import traceback

                                print(traceback.format_exc())

                        if process_died:
                            logging.error(
                                "Worker died for processor %s", myprocessor.name
                            )

                        """ If no worker or the process died, (re)start it """
                        if (
                            myprocessor.requested_status == "start"
                            or (
                                process_died
                                or (
                                    myprocessor.requested_status == "update"
                                    or processor["worker"] is None
                                )
                            )
                            and (
                                myprocessor.status != "stopped"
                                and myprocessor.requested_status != "stopped"
                            )
                        ):
                            logging.debug(
                                "Restarting worker for processor %s because process_died:%s requested:%s worker:%s",
                                myprocessor.name,
                                process_died,
                                myprocessor.requested_status,
                                processor["worker"],
                            )
                            logging.debug("process_died %s", process_died)
                            logging.debug('processor["worker"] %s', processor["worker"])
                            logging.debug(
                                "myprocessor.requested_status %s",
                                myprocessor.requested_status,
                            )
                            logging.debug(
                                "myprocessor.status %s",
                                myprocessor.status,
                            )

                            if processor["worker"] is None:
                                logging.debug("Worker is none")

                            logging.debug("Updating processor")

                            if processor["worker"] is not None:
                                processor["worker"]["process"].kill()
                                processor["worker"] = None

                            if (
                                "deployment" in processor
                                and not inspect(processor["deployment"]).detached
                            ):
                                session.refresh(processor["deployment"])

                            #
                            # If there is a deployment, but no worker
                            #
                            if (
                                "deployment" in processor
                                and mydeployment.worker is None
                            ):
                                """If there is no worker model, find or create one and link to Processor"""

                                logging.debug("WORKER IS NONE. CORRECTING")

                                """ Look for existing worker model in databas e"""
                                worker_model = (
                                    session.query(WorkerModel)
                                    .filter_by(
                                        name=self.agent_service.name
                                        + myprocessor.name
                                        + ".worker"
                                    )
                                    .first()
                                )

                                """ There was no pre-existing worker model in the database """
                                if worker_model is None:
                                    from uuid import uuid4

                                    logging.debug("Creating worker model...")
                                    worker_model = WorkerModel(
                                        id=str(uuid4()),
                                        name=self.agent_service.name
                                        + myprocessor.name
                                        + ".worker",
                                        concurrency=mydeployment.cpus,
                                        status="ready",
                                        backend=self.agent_service.backend,
                                        broker=self.agent_service.broker,
                                        processor=myprocessor,
                                        agent_id=agent.id,
                                        hostname=self.agent_service.name,
                                        requested_status="start",
                                    )
                                    session.add(worker_model)
                                    session.commit()

                                # Attach worker model to deployment
                                mydeployment.worker = worker_model
                                worker_model.lastupdated = datetime.datetime.now()
                                worker_model.status = "running"
                                worker_model.processor = myprocessor
                                mydeployment.status = "starting"
                                session.add(worker_model)

                                logging.debug("Worker model is %s", worker_model)
                                logging.debug("Agent workers is %s", agent.workers)

                                #
                                # Attach worker to agent
                                #
                                if worker_model not in agent.workers:
                                    session.merge(worker_model)
                                    agent.workers += [worker_model]

                                logging.debug("Worker %s created.", worker_model.id)
                                session.commit()

                            """ If there is no process attached to the processor->worker reference """
                            if processor["worker"] is None or process_died:
                                # If there is no worker Process create it
                                worker = {}
                                logging.debug(
                                    "process_died %s and Worker is %s",
                                    process_died,
                                    processor["worker"],
                                )
                                _dir = self.basedir + "/work/" + myprocessor.id

                                os.makedirs(_dir, exist_ok=True)

                                logging.debug(
                                    "Agent: Creating Worker() queue size %s",
                                    self.agent_service.size,
                                )

                                """
                                session.merge(myprocessor)
                                try:
                                    session.add(myprocessor)
                                except:
                                    pass
                                """
                                #
                                # For all my deployments, update processor deployment and create WorkerService
                                #
                                for deployment in myprocessor.deployments:
                                    logger.info(
                                        "Worker is none %s and died %s",
                                        processor["worker"] is None,
                                        process_died,
                                    )

                                    # Only launch worker if we have a deployment for our host
                                    if deployment.hostname == self.agent_service.name:
                                        logging.debug(
                                            "Deployment hostname is {} and HOSTNAME2 is {}".format(
                                                deployment.hostname,
                                                self.agent_service.name,
                                            )
                                        )
                                        processor["deployment"] = deployment
                                        logging.debug(
                                            "-------------------------------------------------------"
                                        )
                                        logging.debug(
                                            f"-----------------------Deploying processor {myprocessor.name}"
                                        )
                                        logging.debug(
                                            f"-----------------------Agent {agent.id}"
                                        )

                                        if self.workerclass:
                                            pass
                                        else:
                                            self.workerclass = WorkerService

                                        if not inspect(myprocessor).detached:
                                            session.expunge(myprocessor)

                                        """ Create the Worker service from a class object """
                                        workerproc = self.workerproc = self.workerclass(
                                            myprocessor,
                                            size=self.agent_service.size,
                                            workdir=_dir,
                                            basedir=self.basedir,
                                            user=self.agent_service.user,
                                            pool=self.agent_service.pool,
                                            port=self.agent_service.workerport,
                                            database=self.agent_service.dburi,
                                            hostname=self.agent_service.name,
                                            agent=agent,
                                            deployment=mydeployment,
                                            celeryconfig=self.agent_service.config,
                                            backend=self.agent_service.backend,
                                            broker=self.agent_service.broker,
                                        )
                                        # TODO: Add to workerproc list

                                        # = workerproc.worker_model
                                        # deployment.worker = workerproc.worker_model
                                        # deployment.worker.processor = processor['processor']
                                        # Setup the virtualenv only
                                        logging.info(
                                            f"-----------------------Starting {myprocessor.name}"
                                        )

                                        """ Build the worker environment """
                                        workerproc.start(start=False)

                                        """ Add the process object to a list """
                                        self.workers += [workerproc]

                                        """ There should be a worker model by now """
                                        worker_model = (
                                            session.query(WorkerModel)
                                            .filter_by(deployment=deployment)
                                            .first()
                                        )

                                        if not worker_model:
                                            logger.error("No worker model present!")
                                            continue

                                        # Launch from the virtualenv
                                        logging.debug(
                                            f"-----------------------Launching {myprocessor.name}"
                                        )

                                        """ Change into my base directory """
                                        os.chdir(self.basedir)

                                        """ Make directories for the worker to work inside of """
                                        if not os.path.exists("work/" + myprocessor.id):
                                            os.makedirs("work/" + myprocessor.id)

                                        os.chdir("work/" + myprocessor.id)

                                        """Launch the task worker"""
                                        logging.debug("Launching from %s", self.basedir)
                                        wprocess = workerproc.launch(
                                            worker_model.name,
                                            agent.name,
                                            agent.hostname,
                                            self.agent_service.pool,
                                        )

                                        """ Update deployment status' and worker reference """
                                        deployment.requested_status = "ready"
                                        deployment.status = "running"
                                        deployment.worker = worker_model
                                        # session.add(deployment.worker)

                                        """ Update worker process reference """
                                        deployment.worker.processor_id = myprocessor.id

                                        try:
                                            # Update worker agent reference
                                            deployment.worker.agent = agent
                                        except:
                                            logging.debug(
                                                "deployment.worker.agent %s",
                                                deployment.worker.agent,
                                            )

                                        logging.debug(
                                            "-----------------------Worker process %s started.",
                                            wprocess.pid,
                                        )

                                        """ Update internal worker reference dictionary """
                                        # worker["model"] = deployment.worker
                                        # worker["model"].process = workerproc.process.pid
                                        worker["process"] = workerproc
                                        worker["wprocess"] = wprocess

                                        """ Update internal process reference dictionary """
                                        processor["worker"] = worker
                                        processor["worker.id"] = deployment.worker.id

                                        logging.debug(
                                            "-----------------------workerproc is %s",
                                            workerproc,
                                        )

                                        # TODO: This might be redundant
                                        self.workers += [worker]

                                        logging.debug(
                                            "-------------------------------------------------------"
                                        )

                            """ Set processor status to running """
                            myprocessor.requested_status = "ready"
                            myprocessor.status = "running"

                            session.commit()

                finally:
                    pass

            session.commit()

    def start(self, agent_service: AgentService, **kwargs):
        from billiard.context import Process

        logger.info("[AgentMonitorPlugin] Starting %s", kwargs)
        self.kwargs = kwargs
        self.agent_service = agent_service
        self.workerclass = kwargs["workerclass"]
        del kwargs["workerclass"]
        self.port = agent_service.port

        with get_session() as session:
            node: Any = (
                session.query(NodeModel)
                .filter_by(name=agent_service.name + ".agent.node")
                .first()
            )
            if not node:
                logging.error("No NODE by name %s", agent_service.name + ".agent.node")
            else:
                agent = (
                    session.query(AgentModel)
                    .filter_by(hostname=agent_service.name)
                    .first()
                )
                if agent is None:
                    agent = AgentModel(
                        hostname=agent_service.name,
                        node_id=node.id,
                        name=agent_service.name + ".agent",
                        pid=os.getpid(),
                        **kwargs,
                    )
                    session.add(agent)

                agent.pid = os.getpid()
                agent.requested_status = "starting"
                agent.status = "starting"
                agent.cpus = self.kwargs["cpus"]
                logging.debug("AgentMonitorPlugin: agent cpus %s", agent.cpus)

        def monitor_processors():
            from datetime import datetime

            processor_workers = []

            """ Main agent loop to monitor state of processors assigned to it and start, stop, pause, resume, kill them
            as their data objects change state. This includes managing the workers and deployments """

            logger.debug(
                "[AgentMonitorPlugin] main_loop processors %s", processor_workers
            )

            process = psutil.Process(os.getpid())

            # Put all the work here
            logging.debug("Agent Service Name %s", agent_service.name)
            logger.debug(
                "[AgentMonitorPlugin] main_loop Worker memory before: %s",
                process.memory_info().rss,
            )

            with get_session() as session:
                """Get myself from database"""
                agent = (
                    session.query(AgentModel)
                    .filter_by(hostname=agent_service.name)
                    .first()
                )
                if agent and agent.requested_status == "kill":
                    import sys

                    logger.info("Killing agent process %s", agent.pid)
                    agent.requested_status = "ready"
                    agent.status = "killed"
                    session.commit()
                    os.kill(agent.pid, signal.SIGINT)
                    os.kill(os.getpid(), signal.SIGINT)
                    sys.exit(0)

                """ If I don't yet exist in database, create me """
                if agent is None:
                    agent = AgentModel(
                        hostname=agent_service.name,
                        name=agent_service.name + ".agent",
                        pid=os.getpid(),
                        **self.kwargs,
                    )

                """ Find a node that might already be associated with me """
                node = (
                    session.query(NodeModel).filter_by(hostname=agent.hostname).first()
                )

                logging.debug("NODE IS %s", node)

                """ Create a new node for me if none exists already """
                if node is None:
                    node = NodeModel(
                        name=agent.name + ".node", agent=agent, hostname=agent.hostname
                    )

                    session.add(node)
                    session.commit()

                """ Add node attributes """
                node.cpus = CPUS
                agent.node = node

                cpu_percent = psutil.cpu_percent()
                mem_total = psutil.virtual_memory().total
                mem_used = psutil.virtual_memory().percent
                mem_free = (
                    psutil.virtual_memory().available
                    * 100
                    / psutil.virtual_memory().total
                )
                node.memsize = str(mem_total)
                node.memused = mem_used
                node.freemem = str(mem_free)
                node.cpuload = cpu_percent

                """ Set my status to running """
                agent.status = "running"
                # agent.cpus = node.cpus
                agent.port = self.port
                agent.updated = datetime.now()
                session.add(node)
                session.commit()

                logger.debug(
                    "[AgentMonitorPlugin] main_loop cpus[%s] agent is %s",
                    agent.cpus,
                    agent,
                )
                logger.debug("[AgentMonitorPlugin] main_loop node is %s", node)

                logger.debug(
                    "[AgentMonitorPlugin] main_loop Worker memory after: %s",
                    process.memory_info().rss,
                )

                # DeploymentMonitor
                logging.debug("Invoking deployment_monitor")

                """ Define core deployment monitoring function """
                self.deployment_monitor(agent)

        gc.collect()

        """ process to monitor deployments """

        def thread_loop():
            import time

            while True:
                monitor_processors()

                time.sleep(10)

        self.process = process = Process(target=thread_loop, daemon=True)
        process.start()

        logger.debug("[AgentMonitorPlugin] Startup Complete")

    def wait(self):
        return self.process.join()


class PluginAgentService(AgentService):
    """Agent class"""

    def __init__(
        self,
        database,
        dburi,
        port=8003,
        config=None,
        clean=False,
        user=None,
        pool=4,
        cpus=-1,
        backend="redis://localhost",
        broker="pyamqp://localhost",
        name=None,
        workerclass=None,
        size=10,
        workerport=-1,
        plugins={},
    ):
        self.port = port
        self.backend = backend
        self.broker = broker
        self.database = database
        self.config = config
        self.pool = pool
        self.cpus = cpus
        self.dburi = dburi
        self.node = None
        self.agent = None
        self.user = user
        self.size = size
        self.workerproc = None
        self.workerport = workerport
        self.workerclass = workerclass
        self.name = name
        self.workers = []
        self.plugins = {}
        self.pluginlist = [
            AgentWebServerPlugin(),
            AgentShutdownPlugin(),
            AgentMonitorPlugin(),
        ]

        logger.info("[PluginAgentService] Init, name %s cpus %s", name, cpus)

        with open("agent.pid", "w") as procfile:
            procfile.write(str(os.getpid()))

    def start(self):
        os.environ["AGENT_CWD"] = os.getcwd()

        for plugin in self.pluginlist:
            self.plugins[plugin.__class__.__name__] = plugin
            logging.debug(
                "AgentService: Registered plugin %s", plugin.__class__.__name__
            )

        kwargs = {"cpus": self.cpus, "workerclass": self.workerclass}
        [plugin.start(self, **kwargs) for plugin in self.pluginlist]

        [plugin.wait() for plugin in self.pluginlist]
