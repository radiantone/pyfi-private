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
import datetime

from typing import List, Literal

logger = logging.getLogger(__name__)    
logger.debug("Agent service")

from threading import Thread
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
            except Exception as ex:
                pass

class AgentPlugin:
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

    def __init__(self, *args, **kwargs):
        import sched
        import time

        self.monitors = {}

        logger.debug("[AgentMonitorPlugin] Creating")
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.processors = []
        self.agent_service = None
        self.workers = []

    def deployment_monitor(self, agent):

        with get_session() as session:
            logger.debug("[DeploymentMonitor] Getting deployments %s",agent.hostname)
            mydeployments = (
                session.query(DeploymentModel)
                    .filter_by(hostname=agent.hostname)
                    .all()
            )
            # Deploy new processors
            for mydeployment in mydeployments:

                logger.debug("GOT DEPLOYMENT %s WORKER %s",mydeployment, mydeployment.worker)
                try:
                    myprocessor = mydeployment.processor
                    logging.debug("MYPROCESSOR %s",myprocessor)
                    #self.database.session.refresh(
                    #    myprocessor
                    #)  # Might not be needed
                    if myprocessor.requested_status == "move":
                        continue

                    for processor in self.processors:
                        processor["processor"] = (
                            session.query(ProcessorModel)
                                .filter_by(id=processor["id"])
                                .first()
                        )
                        logging.debug(processor["processor"])
                        logging.debug(myprocessor)
                        if processor["processor"].id == myprocessor.id:
                            
                            if mydeployment.requested_status == 'update':
                                logging.debug("Deployment %s has changed for processor %s", mydeployment, myprocessor)
                                logging.debug("Updating deployment %s",mydeployment)
                                mydeployment.status = "updating"
                                session.commit()
                                # Restart the worker, which will pull the assigned deployment
                                # from database and restart with new configs
                                logging.info("Killing worker %s",processor["worker"])
                                processor["worker"]["process"].kill()
                                processor["worker"] = None
                                mydeployment.requested_status = 'ready'
                                mydeployment.status = 'running'
                                mydeployment.status = "updating"
                                session.commit()

                    # If I don't already have this processor deployment
                    found = False
                    for processor in self.processors:
                        processor["deployment"] = mydeployment
                        processor["processor"] = (
                            session.query(ProcessorModel)
                                .filter_by(
                                id=processor["id"]
                            ).first()
                        )
                        session.refresh(processor["processor"])
                        if processor["processor"].id == myprocessor.id:
                            # If I already have it in my cache, update it
                            processor["processor"] = myprocessor
                            found = True

                    if not found:
                        # If this is a new processor, add it to cache
                        self.processors += [
                            {"worker": None, "processor": myprocessor, "id": myprocessor.id}
                        ]
                        logging.info("Added processor %s", myprocessor)

                    # This block looks at the processors and creates a worker if needed
                    
                    for processor in self.processors:

                        #
                        # Update processor
                        #
                        '''
                        pid = processor["id"]
                        processor["processor"] = (
                            session.query(ProcessorModel)
                                .filter_by(
                                id=pid
                            ).first()
                        )
                        '''

                        logging.debug(
                            "Processor.requested_status START %s %s",
                            processor["processor"].requested_status, processor["processor"]
                        )

                        if "model" in processor:
                            logger.debug("[PROCESSOR KEYS] is %s %s",processor["model"], processor.keys())
                            
                        process_died = False

                        #
                        # Update worker model
                        #
                        '''
                        if "worker.id" in processor:
                            processor["worker"]["model"] = (
                                session.query(ProcessorModel)
                                    .filter_by(
                                    id=processor["worker.id"]
                                ).first()
                            )
                        '''

                        if "worker" in processor and processor["worker"] and "model" in processor["worker"]:
                            try:
                                session.refresh(processor["worker"]["model"])
                            except:
                                try:
                                    session.add(processor["worker"]["model"])
                                except:
                                    pass


                        #
                        # Processor state events
                        #

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
                                        "Killed worker"
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
                                        "Paused worker"
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
                                        "Paused worker"
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
                                        "Killed worker"
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
                        
                        #
                        # Check if worker is alive
                        #
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

                        #
                        # If no worker or the process died, (re)start it
                        #
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


                            if "deployment" in processor:
                                print("DEPLOYMENT",processor["deployment"])
                                session.refresh(processor["deployment"])
                                print("DEPLOYMENT.WORKER",processor["deployment"].worker)

                            #
                            # If there is a deployment, but no worker
                            #
                            if (
                                    "deployment" in processor
                                    and processor["deployment"].worker is None
                            ):
                                """If there is no worker model, create one and link to Processor"""

                                logging.info("WORKER IS NONE. CORRECTING")
                                
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
                                        processor=processor["processor"],
                                        agent_id=agent.id,
                                        hostname=self.agent_service.name,
                                        requested_status="start",
                                    )
                                    session.add(worker_model)
                                    session.commit()

                                # Attach worker model to deployment
                                processor["deployment"].worker = worker_model
                                worker_model.lastupdated = datetime.datetime.now()
                                worker_model.status = "running"
                                worker_model.processor = processor["processor"]
                                
                                #session.add(agent)
                                session.add(worker_model)

                                logging.info("Worker model is %s", worker_model)
                                logging.info(
                                    "Agent workers is %s", agent.workers
                                )

                                #
                                # Attach worker to agent
                                #
                                agent.workers += [worker_model]

                                logging.info("Worker %s created.", worker_model.id)
                                session.commit()

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
                                
                                #
                                # For all my deployments, update processor deployment and create WorkerService
                                #
                                for deployment in processor["processor"].deployments:
                                    logger.debug("Worker is none %s and died %s",processor["worker"] is None, process_died)
                                    logging.debug("Deployment worker %s", deployment)
                                    # Only launch worker if we have a deployment for our host
                                    if deployment.hostname == self.agent_service.name:
                                        logging.debug(
                                            "Deployment hostname is {} and HOSTNAME2 is {}".format(
                                                deployment.hostname, self.agent_service.name
                                            )
                                        )
                                        processor["deployment"] = deployment
                                        logging.debug(
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

                                        # session.add(workerproc.worker_model)
                                        worker_model = (
                                            session.query(WorkerModel)
                                                .filter_by(
                                                deployment=deployment
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
                                            agent.hostname,
                                            self.agent_service.pool,
                                        )

                                        deployment.requested_status = "ready"
                                        deployment.status = "running"
                                        deployment.worker = worker_model
                                        # session.add(deployment.worker)
                                        deployment.worker.processor_id = processor[
                                            "processor"
                                        ].id
                                        try:
                                            deployment.worker.agent = agent
                                        except:
                                            logging.info("deployment.worker.agent %s",deployment.worker.agent)

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
                                        processor["worker.id"] = worker["model"].id
                                        print("**** PROCESS WORKER 2",processor["worker"])
                                        logging.info(
                                            "-----------------------workerproc is %s",
                                            workerproc,
                                        )

                                        self.workers += [worker]

                                        logging.info(
                                            "-------------------------------------------------------"
                                        )

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "running"

                            #session.add(processor["processor"])
                            #session.refresh(processor["processor"])

                            #session.commit()
                    
                    
                finally:
                    pass

    def start(self, agent_service: AgentService, **kwargs):
        from billiard.context import Process
        logger.info("[AgentMonitorPlugin] Starting %s",kwargs)
        self.kwargs = kwargs
        self.agent_service = agent_service

        self.port = agent_service.port

        with get_session() as session:
            node = (
                session.query(NodeModel).filter_by(name=agent_service.name+".agent.node").first()
            )
            if not node:
                logging.error("No NODE by name %s",agent_service.name+".agent.node")
            else:
                agent = (
                    session.query(AgentModel).filter_by(hostname=agent_service.name).first()
                )
                if agent is None:
                    agent = AgentModel(
                        hostname=agent_service.name, node_id=node.id, name=agent_service.name + ".agent", pid=os.getpid(), **kwargs
                    )
                    session.add(agent)

                agent.pid = os.getpid()
                agent.requested_status = "starting"
                agent.status = "starting"
                agent.cpus = self.kwargs['cpus']
                logging.info("AgentMonitorPlugin: agent cpus %s",agent.cpus)

        def update_queues():
            from pyfi.util.rabbit import get_queues
            import redis
            import json

            queues = get_queues()
            logging.debug("QUEUES %s",queues)
            redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

            redisclient.publish(
                "global",
                json.dumps({'type':'queues','queues':queues}),
            )
            redisclient.publish(
                "queues",
                json.dumps({'type':'queues','queues':queues}),
            )

        def monitor_processors():
            import sched
            from datetime import datetime

            processor_workers = []

            """ Main agent loop to monitor state of processors assigned to it and start, stop, pause, resume, kill them
            as their data objects change state. This includes managing the workers and deployments """

            logger.debug("[AgentMonitorPlugin] main_loop processors %s", processor_workers)

            process = psutil.Process(os.getpid())
            
            with get_session() as session:
                # Put all the work here
                logging.debug("Agent Service Name %s",agent_service.name)
                logger.debug("[AgentMonitorPlugin] main_loop Worker memory before: %s",process.memory_info().rss)
                # Get or create Agent
                agent = (
                    session.query(AgentModel).filter_by(hostname=agent_service.name).first()
                )
                if agent and agent.requested_status == 'kill':
                    import sys
                    logger.info("Killing agent process %s", agent.pid)
                    agent.requested_status = 'ready'
                    agent.status = 'killed'
                    session.commit()
                    os.kill(agent.pid, signal.SIGINT)
                    os.kill(os.getpid(), signal.SIGINT)
                    sys.exit(0)

                # Get or create Node for this agent
                if agent is None:
                    agent = AgentModel(
                        hostname=agent_service.name, name=agent_service.name + ".agent", pid=os.getpid(), **self.kwargs
                    )

                if agent is None:
                    logger.error("No agent present.")
                    
                    return

                node = (
                    session.query(NodeModel).filter_by(hostname=agent.hostname).first()
                )
                logging.debug("NODE IS %s",node)
                if node is None:
                    node = NodeModel(
                        name=agent.name + ".node", agent=agent, hostname=agent.hostname
                    )
                    
                    session.add(node)
                    session.commit()

                node.cpus = CPUS
                agent.node = node
            
                agent.status = "running"
                #agent.cpus = node.cpus
                agent.port = self.port
                agent.updated = datetime.now()

                logger.debug("[AgentMonitorPlugin] main_loop cpus[%s] agent is %s",agent.cpus, agent)
                logger.debug("[AgentMonitorPlugin] main_loop node is %s",node)
                
                logger.debug("[AgentMonitorPlugin] main_loop Worker memory after: %s",process.memory_info().rss)

                # DeploymentMonitor
                logging.debug("Invoking deployment_monitor")
                self.deployment_monitor(agent)



            # ProcessorMonitor



            # NodeMonitor


            gc.collect()

        def thread_loop():
            while True:
                import time

                update_queues()
                monitor_processors()

                time.sleep(3)

        self.process = process = Process(target=thread_loop, daemon=True)
        process.start()

        logger.debug("[AgentMonitorPlugin] Startup Complete")
        
    def wait(self):
        return self.process.join()

plugins = [AgentWebServerPlugin(), AgentShutdownPlugin(), AgentMonitorPlugin()]

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
