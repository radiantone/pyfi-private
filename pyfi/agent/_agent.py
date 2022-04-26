"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import logging
# logging.basicConfig(level=logging.DEBUG)
import configparser
import multiprocessing
import os
import gc
import platform
import shutil
import signal
import psutil

from typing import List, Literal

logger = logging.getLogger(__name__)    
logger.debug("Agent service")

from multiprocessing import Condition
from contextlib import contextmanager
from pathlib import Path

from flask import Flask
from sqlalchemy import create_engine, MetaData, literal_column
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy_oso import authorized_sessionmaker
from pyfi.blueprints.show import blueprint
from pyfi.db.model import WorkerModel, AgentModel, NodeModel, DeploymentModel, ProcessorModel
from pyfi.worker import WorkerService

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

engine = create_engine(CONFIG.get("database", "uri"))

@app.route("/")
def health():
    import json

    return json.dumps({"status": "green"})

def import_class(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

@contextmanager
def get_session(**kwargs):
    logger.debug("get_session: Creating session")
    session = sessionmaker(bind=engine, **kwargs)() #expire_on_commit=False

    try:
        logger.debug("get_session: Yielding session")
        yield session
    except:
        logger.debug("get_session: Rollback session")
        session.rollback()
        raise
    else:
        logger.debug("get_session: Commit session")
        session.commit()
    finally:
        logger.debug("get_session: Closing session")
        session.expunge_all()
        session.close()
        gc.collect()

def kill_containers():
    """Kill running containers"""
    import docker

    if 'AGENT_CWD' in os.environ:
        agent_cwd = os.environ["AGENT_CWD"]

        if os.path.exists(f"{agent_cwd}/containers.pid"):
            client = docker.from_env()
            logger.info("Found containers.pid")
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
            except Exception as ex:
                pass

class AgentPlugin:
    pass

class MonitorPlugin:
    pass

class AgentService:
    dburi : str = "postgresql://postgres:postgres@" + HOSTNAME + ":5432/pyfi"
    port : int = 8003,
    config = None,
    clean : bool = False,
    user = None,
    pool : int = 4,
    cpus : int = -1,
    backend : str = "redis://localhost",
    broker : str = "pyamqp://localhost",
    name : str = None,
    size : int = 10,
    plugins : List[AgentPlugin] = [],
    workerport : int = 8020

class ProcessorMonitor(MonitorPlugin):
    """ Monitor list of processors assigned to this node """
    workers = []

    def __init__(self, agent_service : AgentService):
        logger.debug("[ProcessorMonitor] Create")
        self.agent_service = agent_service

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):
        from datetime import datetime
        from uuid import uuid4

        logger.debug("[ProcessorMonitor] Monitor")

        with get_session(expire_on_commit=False) as session:

            logger.info("Processors %s",processors)
            mydeployments = (
                session.query(DeploymentModel)
                    .filter_by(hostname=agent.hostname)
                    .all()
            )
            if 'AgentMonitorPlugin' in self.agent_service.plugins and \
            'DeploymentMonitor' in self.agent_service.plugins['AgentMonitorPlugin'].monitors:
                lock = self.agent_service.plugins['AgentMonitorPlugin'].monitors['DeploymentMonitor'].lock
                logger.debug("[ProcessorMonitor] Acquiring lock ")
                lock.acquire()
                logger.debug("[ProcessorMonitor] Got lock ")
                try:
                    processors = self.agent_service.plugins['AgentMonitorPlugin'].monitors['DeploymentMonitor'].processors
                    
                    for processor in processors:
                        session.merge(processor["processor"])
                        session.merge(processor["processor"])
                        
                        logging.info("QUERYING PROCESSOR ID %s",processor["processor"].id)
                        processor["processor"] = (
                            session.query(ProcessorModel)
                                .filter_by(
                                id=processor["processor"].id
                            ).first()
                        )
                        logging.info("GOT PROCESSOR %s",processor["processor"])
                        #session.add(processor["processor"])
                        #session.refresh(processor["processor"])
                        # Check if I already have a deployment
                        found = False
                        for deployment in mydeployments:
                            logger.info("[ProcessorMonitor] Deployment %s %s %s", processor["processor"].name, processor["processor"], deployment.processor)
                            if deployment.processor.id == processor["processor"].id:
                                found = True
                                break

                        agent_cwd = os.environ["AGENT_CWD"]

                        # If I have no deployment for the current processor, undeploy it
                        if not found:
                            logger.info("Processor no longer deployed")

                            if processor["worker"] is not None:
                                logging.info(
                                    f"Killing processor {processor['processor'].name}."
                                )
                                processor["worker"]["process"].kill()
                                processor["worker"] = None
                                processors.remove(processor)
                                logging.info(
                                    "Removed processor {} from list.".format(
                                        processor["processor"].name
                                    )
                                )

                                if os.path.exists(
                                        f"{agent_cwd}/{processor['processor'].name}.pid"
                                ):
                                    import docker

                                    with open(
                                            f"{agent_cwd}/{processor['processor'].name}.pid",
                                            "r",
                                    ) as pidfile:
                                        container_id = pidfile.read()
                                        client = docker.from_env()
                                        container = client.containers.get(
                                            container_id.strip()
                                        )
                                        logging.info(
                                            f"Killing worker container {container_id}"
                                        )
                                        container.kill()

                finally:
                    lock.release()
                    logger.debug("[ProcessorMonitor] Freed lock ")

class WorkerMonitor(MonitorPlugin):
    """ Monitor list of workers under this agent """
    def __init__(self):
        logger.debug("[WorkerMonitor] Create")

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):
        logger.debug("[WorkerMonitor] Monitor")

        if session:
            logging.info("WorkerMonitor %s",processors)

class DeploymentMonitor(MonitorPlugin):
    """ Monitor deployment records for this agent and deploy workers as needed """
    agent_service : AgentService
    processors = []
    workers = []

    lock = Condition()

    def __init__(self, agent_service : AgentService):
        logger.debug("[DeploymentMonitor] Create")
        self.agent_service = agent_service

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):

        logger.debug("[DeploymentMonitor] Monitor")

        if CONFIG.has_section("services"):
            if CONFIG.has_option("services", "worker"):
                worker_class_name = CONFIG.get("services","worker")
                worker_class=import_class(worker_class_name)
            else:
                worker_class=WorkerService
        
        gc.collect()
        process = psutil.Process(os.getpid())
        logger.debug("[DeploymentMonitor] memory used %s",process.memory_info().rss)

        with get_session(expire_on_commit=False) as session:
            logger.debug("[DeploymentMonitor] Getting deployments %s",agent.hostname)
            mydeployments = (
                session.query(DeploymentModel)
                    .filter_by(hostname=agent.hostname)
                    .all()
            )
            agent = (
                session.query(AgentModel).filter_by(id=agent.id).first()
            )
            # Deploy new processors
            for mydeployment in mydeployments:

                self.lock.acquire()
                try:
                    myprocessor = mydeployment.processor
                    #self.database.session.refresh(
                    #    myprocessor
                    #)  # Might not be needed
                    if myprocessor.requested_status == "move":
                        continue

                    # If I don't already have this processor deployment
                    found = False
                    for processor in self.processors:
                        session.merge(myprocessor)
                        session.merge(processor["processor"])
                        session.add(myprocessor)
                        session.refresh(myprocessor)
                        processor["processor"] = (
                            session.query(ProcessorModel)
                                .filter_by(
                                id=processor["processor"].id
                            ).first()
                        )
                        if processor["processor"].id == myprocessor.id:
                            # If I already have it in my cache, update it
                            processor["processor"] = myprocessor
                            found = True

                    if not found:
                        # If this is a new processor, add it to cache
                            self.processors += [
                                {"worker": None, "processor": myprocessor}
                            ]
                            logging.info("Added processor %s", myprocessor)

                    for processor in self.processors:
                        pid = processor["processor"].id
                        processor["processor"] = (
                            session.query(ProcessorModel)
                                .filter_by(
                                id=pid
                            ).first()
                        )

                        logging.debug(
                            "Processor.requested_status START %s",
                            processor["processor"].requested_status,
                        )
                        logger.debug("[WORKER] is %s",processor["worker"])
                        worker_id = processor["worker"]["model"].id if "worker" in processor and processor["worker"] else None

                        if processor["processor"].requested_status == "removed":
                            if processor["worker"] is not None:
                                logging.info("Killing worker")
                                try:
                                    processor["worker"]["process"].kill()
                                    processor["worker"] = None
                                    logging.info("Killed worker")
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["delete"] = True

                            session.delete(processor["deployment"].worker)
                            session.delete(processor["deployment"])

                            if os.path.exists("work/" + processor["processor"].id):
                                logging.debug(
                                    "Removing work directory %s",
                                    "work/" + processor["processor"],
                                )
                                shutil.rmtree("work/" + processor["processor"])

                            logging.info("Processor is removed")

                            continue

                        if processor["processor"].requested_status == "restart":
                            if processor["worker"] is not None:
                                logging.info("Killing worker")
                                try:
                                    
                                    processor["worker"]["process"].kill()
                                    processor["worker"] = None
                                    logging.info(
                                        "Killed worker %s", worker_id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "start"
                            processor["processor"].status = "stopped"
                            processor["deployment"].worker.status = "stopped"
                            processor["deployment"].worker.requested_status = "ready"
                            processor["status"] = "stopped"

                            logging.info("Processor is stopped")

                            session.add(processor["deployment"].worker)
                            session.add(processor["processor"])

                        if processor["processor"].requested_status == "paused":
                            if processor["worker"] is not None:
                                logging.info("Pausing worker")
                                try:
                                    processor["worker"]["process"].suspend()
                                    logging.info(
                                        "Paused worker %s", worker_id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "paused"
                            processor["deployment"].worker.status = "paused"
                            processor["deployment"].worker.requested_status = "ready"

                            logging.info("Processor is paused")

                            session.add(processor["deployment"].worker)
                            session.add(processor["processor"])

                            continue

                        if processor["processor"].requested_status == "resumed":
                            if processor["worker"] is not None:
                                logging.info("Resuming worker")
                                try:
                                    processor["worker"]["process"].resume()
                                    logging.info(
                                        "Paused worker %s", worker_id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "resumed"
                            processor["deployment"].worker.status = "resumed"
                            processor["deployment"].worker.requested_status = "ready"

                            logging.info("Processor is resumed")

                            session.add(processor["deployment"].worker)
                            session.add(processor["processor"])

                            continue

                        if processor["processor"].requested_status == "stopped":
                            if processor["worker"] is not None:
                                logging.info("Killing worker")
                                try:
                                    processor["worker"]["process"].kill()
                                    processor["worker"] = None
                                    logging.info(
                                        "Killed worker %s", worker_id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "stopped"
                            processor["deployment"].worker.status = "stopped"
                            processor["deployment"].worker.requested_status = "ready"

                            logging.info("Processor is stopped")

                            session.add(processor["deployment"].worker)
                            session.add(processor["processor"])

                        if processor["processor"].requested_status == "started":
                            if processor["worker"] is None:
                                # Spin up worker if I have CPU's available
                                # Create a worker, link it to the processor
                                # Add it to workers list
                                pass

                        """
                        If the worker python Process is no longer alive, restart it as long as the processor is not in stopped state.
                        Otherwise, if processor requested state is 'update', then restart process
                        or if processor worker is None, restart it (e.g. on startup)
                        """
                        process_died = False
                        if "worker" in processor:
                            try:
                                # process_died = not processor['worker']['wprocess'].is_alive()
                                logging.debug(
                                    "Processor.requested_status 0 %s",
                                    processor["processor"].requested_status,
                                )
                                logging.debug(
                                    "processor['worker'] is %s", processor["worker"]
                                )
                                if (
                                        processor["worker"]
                                        and processor["worker"]["wprocess"]
                                ):
                                    process_died = (
                                            processor["worker"]["wprocess"].poll()
                                            is not None
                                    )
                            except:
                                import traceback

                                print(traceback.format_exc())

                        if process_died:
                            logging.error("Process died!")

                        if (
                                processor["processor"].requested_status == "start"
                                or (
                                process_died
                                or (
                                        processor["processor"].requested_status == "update"
                                        or processor["worker"] is None
                                )
                        )
                                and (
                                processor["processor"].status != "stopped"
                                and processor["processor"].requested_status != "stopped"
                        )
                        ):

                            logging.debug("process_died %s", process_died)
                            logging.debug("processor[\"worker\"] %s", processor["worker"])
                            logging.debug("processor[\"processor\"].requested_status %s", processor["processor"].requested_status)
                            logging.debug("processor[\"processor\"].status %s", processor["processor"].status)

                            if processor["worker"] is None:
                                logging.info("Worker is none")

                            logging.info("Updating processor")

                            if processor["worker"] is not None:
                                processor["worker"]["process"].kill()
                                processor["worker"] = None

                            """
                            TODO: Separate out the worker process into `pyfi worker start --name <name>` so it can be run in its own virtualenv as a child process here
                            This will allow the gitrepo to be installed in the virtualenv for that processor and kept separate from this agent environment
                            Once a WorkerModel has been created with all the details, spawn `pyfi worker start` FROM the virtualenv after the gitrepo setup.py has been
                            installed.
                            """
                            if (
                                    "deployment" in processor
                                    and processor["deployment"].worker is None
                            ):
                                """If there is no worker model, create one and link to Processor"""

                                # TODO: Not sure this is needed since worker now puts worker model row in database
                                worker_model = (
                                    session.query(WorkerModel)
                                        .filter_by(
                                        name=self.agent_service.name
                                                + ".agent."
                                                + processor["processor"].name
                                                + ".worker"
                                    )
                                        .first()
                                )

                                if worker_model is None:
                                    from uuid import uuid4

                                    logging.info("Creating worker model...")
                                    worker_model = WorkerModel(
                                        id=str(uuid4()),
                                        name=self.agent_service.name
                                                + ".agent."
                                                + processor["processor"].name
                                                + ".worker",
                                        concurrency=processor["deployment"].cpus,
                                        status="ready",
                                        backend=self.agent_service.backend,
                                        broker=self.agent_service.broker,
                                        agent_id=agent.id,
                                        hostname=self.agent_service.name,
                                        requested_status="start",
                                    )

                                processor["deployment"].worker = worker_model
                                worker_model.lastupdated = datetime.now()
                                worker_model.status = "running"
                                worker_model.processor = processor["processor"]
                                
                                session.add(agent)
                                session.add(worker_model)
                                logging.info("Worker model is %s", worker_model)
                                logging.info(
                                    "Agent worker is %s", agent.worker
                                )
                                agent.workers += [worker_model]

                                logging.info("Worker %s created.", worker_model.id)

                            if processor["worker"] is None or process_died:
                                # If there is no worker Process create it
                                worker = {}
                                logging.info(
                                    "process_died %s and Worker is %s",
                                    process_died,
                                    processor["worker"],
                                )
                                _dir = "work/" + processor["processor"].id

                                os.makedirs(_dir, exist_ok=True)

                                logging.info(
                                    "Agent: Creating Worker() queue size %s", self.agent_service.size
                                )
                                session.merge(processor["processor"])
                                try:
                                    session.add(processor["processor"])
                                except:
                                    pass
                                
                                for deployment in processor["processor"].deployments:
                                    logger.info("Worker is none %s and died %s",processor["worker"] is None, process_died)
                                    logging.info("Deployment worker %s", deployment)
                                    # Only launch worker if we have a deployment for our host
                                    if deployment.hostname == self.agent_service.name:
                                        logging.info(
                                            "Deployment hostname is {} and HOSTNAME is {}".format(
                                                deployment.hostname, HOSTNAME
                                            )
                                        )
                                        processor["deployment"] = deployment
                                        logging.info(
                                            "-------------------------------------------------------"
                                        )
                                        logging.info(
                                            f"-----------------------Deploying processor {processor['processor'].name}"
                                        )
                                        logging.info(
                                            f"-----------------------Agent {agent.id}"
                                        )
                                        workerproc = self.workerproc = WorkerService(
                                            processor["processor"],
                                            size=self.agent_service.size,
                                            workdir=_dir,
                                            user=self.agent_service.user,
                                            pool=self.agent_service.pool,
                                            workerport=self.agent_service.workerport,
                                            database=self.agent_service.dburi,
                                            hostname=self.agent_service.name,
                                            agent=agent,
                                            deployment=deployment,
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
                                            f"-----------------------Starting {processor['processor'].name}"
                                        )
                                        workerproc.start(start=False)

                                        self.workers += [workerproc]

                                        print("**** PROCESS WORKER 1",processor["worker"])
                                        # session.add(workerproc.worker_model)
                                        worker_model = (
                                            session.query(WorkerModel)
                                                .filter_by(
                                                name=self.agent_service.name
                                                        + ".agent."
                                                        + processor["processor"].name
                                                        + ".worker"
                                            )
                                                .first()
                                        )

                                        if not worker_model:
                                            logger.error("No worker model present!")
                                            continue

                                        # Launch from the virtualenv
                                        logging.info(
                                            f"-----------------------Launching {processor['processor'].name}"
                                        )
                                        wprocess = workerproc.launch(
                                            worker_model.name,
                                            agent.name,
                                            HOSTNAME,
                                            self.agent_service.pool,
                                        )

                                        deployment.requested_status = "ready"
                                        deployment.status = "running"
                                        deployment.worker = worker_model
                                        # session.add(deployment.worker)
                                        deployment.worker.processor_id = processor[
                                            "processor"
                                        ].id
                                        deployment.worker.agent = agent

                                        logging.info(
                                            "-----------------------Worker process %s started.",
                                            wprocess.pid,
                                        )

                                        worker["model"] = deployment.worker
                                        worker[
                                            "model"
                                        ].process = workerproc.process.pid
                                        worker["process"] = workerproc
                                        worker["wprocess"] = wprocess

                                        processor["worker"] = worker
                                        print("**** PROCESS WORKER 2",processor["worker"])
                                        logging.info(
                                            "-----------------------workerproc is %s",
                                            workerproc,
                                        )

                                        #self.workers += [worker]

                                        logging.info(
                                            "-------------------------------------------------------"
                                        )

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "running"

                            session.add(processor["processor"])
                
                finally:
                    self.lock.release()

class NodeMonitor(MonitorPlugin):
    """ Monitor this node and update it as attributes change """
    def __init__(self):
        logger.debug("[NodeMonitor] Create")

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):
        from datetime import datetime
        import psutil

        logger.debug("[NodeMonitor] Monitor")
        vmem = psutil.virtual_memory()

        node : NodeModel = agent.node

        node.memsize = vmem.total
        node.freemem = vmem.free
        node.memused = vmem.percent

        agent.status = "running"
        #agent.cpus = node.cpus
        agent.updated = datetime.now()

class AgentWebServerPlugin(AgentPlugin):
    """ Health check web endpoint """
    def __init__(self):
        logger.debug("[AgentWebServerPlugin] Creating")
        pass

    def start(self, agent: AgentService, **kwargs):

        logger.debug("[AgentWebServerPlugin] Starting")
        import bjoern
        from billiard.context import Process
        #########################################################################
        # Agent endpoints & health checks
        #########################################################################
        def web_server():
            from setproctitle import setproctitle

            try:
                setproctitle("pyfi agent::web_server")
                logger.info("Starting web server on %s", agent.port)
                bjoern.run(app, "0.0.0.0", agent.port)
            except Exception as ex:
                logging.error(ex)
                logger.info("web_server: exiting...")

        self.process = webserver = Process(target=web_server, daemon=True)
        webserver.start()
        logger.debug("[AgentWebServerPlugin] Startup Complete")

    def wait(self):
        return self.process.join()

class AgentShutdownPlugin(AgentPlugin):
    """ Detect signal and gracefully shutown """
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
                child.kill()

            logger.info("CWD is %s %s", os.getcwd(), os.environ["AGENT_CWD"])

            agent_cwd = os.environ["AGENT_CWD"]

            logger.info("Killing workers")

            with get_session() as session:
                agent = (
                    session.query(AgentModel).filter_by(hostname=agent_service.name).first()
                )
                for worker in agent_service.plugins['AgentMonitorPlugin'].monitors['ProcessorMonitor'].workers:
                    logger.info("Killing worker %s", worker)
                    worker.kill()

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
    """ Master plugin for all the monitor classes """
    def __init__(self,):
        import sched
        import time

        self.monitors = {}

        logger.debug("[AgentMonitorPlugin] Creating")
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def start(self, agent_service: AgentService, **kwargs):
        from billiard.context import Process
        logger.info("[AgentMonitorPlugin] Starting %s",kwargs)
        self.kwargs = kwargs
        
        with get_session() as session:
            agent = (
                session.query(AgentModel).filter_by(hostname=agent_service.name).first()
            )
            if agent is None:
                agent = AgentModel(
                    hostname=agent_service.name, name=agent_service.name + ".agent", pid=os.getpid(), **kwargs
                )

            agent.pid = os.getpid()
            agent.requested_status = "starting"
            agent.status = "starting"
            agent.cpus = self.kwargs['cpus']

            logging.info("AgentMonitorPlugin: agent cpus %s",agent.cpus)
        # Create a list of pluggable "Monitor" objects that perform various independent tasks
        monitors = [ProcessorMonitor(agent_service), DeploymentMonitor(agent_service)] #, DeploymentMonitor(agent_service), NodeMonitor()]

        for monitor in monitors:
            self.monitors[monitor.__class__.__name__] = monitor
            logging.debug("AgentMonitorPlugin: Registered monitor %s",monitor.__class__.__name__)

        def monitor_processors():
            import sched
            from datetime import datetime

            processor_workers = []

            def main_loop(monitors, **kwargs):
                """ Main agent loop to monitor state of processors assigned to it and start, stop, pause, resume, kill them
                as their data objects change state. This includes managing the workers and deployments """

                logger.debug("[AgentMonitorPlugin] main_loop run %s %s", monitors, kwargs)
                logger.debug("[AgentMonitorPlugin] main_loop processors %s", processor_workers)

                process = psutil.Process(os.getpid())
                with get_session() as session:
                    logger.debug("[AgentMonitorPlugin] main_loop Worker memory before: %s",process.memory_info().rss)
                    # Get or create Agent
                    agent = (
                        session.query(AgentModel).filter_by(hostname=agent_service.name).first()
                    )
                    # Get or create Node for this agent
                    if agent is None:
                        # Create database ping process to notify pyfi that I'm here and active
                        # agent process will monitor database and manage worker process pool
                        # agent will report local available resources to database
                        # agent will report # of active processors/CPUs and free CPUs
                        agent = AgentModel(
                            hostname=agent_service.name, name=agent_service.name + ".agent", pid=os.getpid(), **self.kwargs
                        )

                    if agent is None:
                        logger.error("No agent present.")
                        self.scheduler.enter(
                            3,
                            1,
                            main_loop,
                            argument=(monitors,),
                            kwargs=kwargs
                        )
                        return

                    node = (
                        session.query(NodeModel).filter_by(hostname=agent.hostname).first()
                    )

                    if node is None:
                        node = NodeModel(
                            name=agent.name + ".node", agent=agent, hostname=agent.hostname
                        )
                        
                        session.add(node)

                    node.cpus = CPUS
                    agent.node = node
                
                    agent.status = "running"
                    #agent.cpus = node.cpus
                    #agent.port = self.port
                    agent.updated = datetime.now()

                    logger.info("[AgentMonitorPlugin] main_loop cpus[%s] agent is %s",agent.cpus, agent)
                    logger.info("[AgentMonitorPlugin] main_loop node is %s",node)
                    
                    logger.debug("[AgentMonitorPlugin] main_loop Worker memory after: %s",process.memory_info().rss)

                    # Get or create Node for this agent
                    _node = {}
                    # Get Processors for this agent
                    processors = []
                    # Get deployments for this host
                    deployments = []

                    [monitor.monitor(agent, processors, deployments) for monitor in monitors]

                    gc.collect()

                self.scheduler.enter(
                    3,
                    1,
                    main_loop,
                    argument=(monitors,),
                    kwargs=kwargs
                )



            self.scheduler.enter(
                3,
                1,
                main_loop,
                argument=(monitors,),
                kwargs={}
            )

            self.scheduler.run()

        self.process = process = Process(target=monitor_processors, daemon=True)
        process.start()
        logger.debug("[AgentMonitorPlugin] Startup Complete")
        
    def wait(self):
        return self.process.join()

plugins = [AgentWebServerPlugin(), AgentShutdownPlugin(), AgentMonitorPlugin()]

# noinspection PyPep8
class PluginAgentService(AgentService):
    """ Agent class """

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
            size=10,
            workerport=8020,
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
        self.name = name
        self.workers = []
        self.plugins = {}

        logger.info("[PluginAgentService] Init, name %s cpus %s", name, cpus)

        with open("agent.pid", "w") as procfile:
            procfile.write(str(os.getpid()))
            
    def start(self):

        os.environ["AGENT_CWD"] = os.getcwd()
        from datetime import datetime

        for plugin in plugins:
            self.plugins[plugin.__class__.__name__] = plugin
            logging.debug("AgentService: Registered plugin %s",plugin.__class__.__name__)

        kwargs = {
            'cpus':self.cpus
        }
        [plugin.start(self, **kwargs) for plugin in plugins]

        [plugin.wait() for plugin in plugins]
