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
        pass
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

            def monitor_processors():
                import sched
                from datetime import datetime

                processor_workers = []

                def main_loop(*args, **kwargs):
                    """ Main agent loop to monitor state of processors assigned to it and start, stop, pause, resume, kill them
                    as their data objects change state. This includes managing the workers and deployments """

                    logger.debug("[AgentMonitorPlugin] main_loop processors %s", processor_workers)

                    process = psutil.Process(os.getpid())
                   
                    # Put all the work here

                    # DeploymentMonitor



                    # ProcessorMonitor



                    # NodeMonitor


                    gc.collect()

                    self.scheduler.enter(
                        3,
                        1,
                        main_loop,
                        kwargs=kwargs
                    )


                self.scheduler.enter(
                    3,
                    1,
                    main_loop,
                    kwargs={}
                )

                self.scheduler.run()

            self.process = process = Process(target=monitor_processors, daemon=True)
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
