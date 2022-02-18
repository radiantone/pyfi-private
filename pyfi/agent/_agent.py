"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import configparser
import glob
import logging
# logging.basicConfig(level=logging.DEBUG)
import multiprocessing
import os
import gc
import platform
import shutil
import signal
import psutil

from contextlib import contextmanager
from pathlib import Path

from flask import Flask
from sqlalchemy import create_engine, MetaData, literal_column
from sqlalchemy import exc as sa_exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy_oso import authorized_sessionmaker
from pyfi.blueprints.show import blueprint
from pyfi.db.model import WorkerModel, AgentModel, NodeModel, DeploymentModel
from pyfi.worker import WorkerService

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

def kill_containers():
    """Kill running containers"""
    import docker

    if 'AGENT_CWD' in os.environ:
        agent_cwd = os.environ["AGENT_CWD"]

        if os.path.exists(f"{agent_cwd}/containers.pid"):
            client = docker.from_env()
            logging.info("Found containers.pid")
            with open(f"{agent_cwd}/containers.pid", "r") as cfile:
                pids = cfile.readlines()
                for pid in pids:
                    try:
                        logging.info("Getting client container %s", pid)
                        container = client.containers.get(pid.strip())
                        logging.info("Killing container...")
                        container.kill()
                        logging.info("Done")
                    except Exception as ex:
                        logging.error("Error obtaining or killing container %s", pid)

            try:
                os.remove(f"{agent_cwd}/containers.pid")
            except Exception as ex:
                pass

class AgentService:
    name = None

class MonitorPlugin:
    pass

class ProcessorMonitor(MonitorPlugin):

    def __init__(self):
        logging.debug("[ProcessorMonitor] Create")

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):
        logging.debug("[ProcessorMonitor] Monitor")

        if session:
            _processors = []

class DeploymentMonitor(MonitorPlugin):

    def __init__(self):
        logging.debug("[DeploymentMonitor] Create")

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):
        logging.debug("[DeploymentMonitor] Monitor")

        if session:
            logging.debug("[DeploymentMonitor] Getting deployments %s",agent.hostname)
            mydeployments = (
                session.query(DeploymentModel)
                    .filter_by(hostname=agent.hostname)
                    .all()
            )

            for deployment in mydeployments:
                logging.debug("Deployment %s", deployment)

class NodeMonitor(MonitorPlugin):

    def __init__(self):
        logging.debug("[NodeMonitor] Create")

    def monitor(self, agent: AgentModel, processors: list, deployments: list, session=None):
        from datetime import datetime
        import psutil

        logging.debug("[NodeMonitor] Monitor")
        vmem = psutil.virtual_memory()

        node : NodeModel = agent.node

        node.memsize = vmem.total
        node.freemem = vmem.free
        node.memused = vmem.percent

        agent.status = "running"
        agent.cpus = node.cpus
        agent.updated = datetime.now()

        if session:
            pass

class AgentWebServerPlugin:

    def __init__(self):
        logging.debug("[AgentWebServerPlugin] Creating")
        pass

    def start(self, agent: AgentService):

        logging.debug("[AgentWebServerPlugin] Starting")
        import bjoern
        from billiard.context import Process
        #########################################################################
        # Agent endpoints & health checks
        #########################################################################
        def web_server():
            from setproctitle import setproctitle

            try:
                setproctitle("pyfi agent::web_server")
                logging.info("Starting web server on %s", agent.port)
                bjoern.run(app, "0.0.0.0", agent.port)
            except Exception as ex:
                logging.error(ex)
                logging.info("web_server: exiting...")

        self.process = webserver = Process(target=web_server, daemon=True)
        webserver.start()
        logging.debug("[AgentWebServerPlugin] Startup Complete")

    def wait(self):
        return self.process.join()

class AgentShutdownPlugin:

    def __init__(self):
        logging.debug("[AgentShutdownPlugin] Creating")

    def start(self, agent: AgentService):
        logging.debug("[AgentShutdownPlugin] Starting")
        def shutdown(*args):
            """Shutdown worker"""
            from psutil import Process

            kill_containers()
            logging.info("Shutting down agent...")
            process = Process(os.getpid())

            logging.info("    Terminating child processes...")
            for child in process.children(recursive=True):
                logging.info(
                    "         Process pid {}: Killing child {}".format(
                        process.pid, child.pid
                    )
                )
                child.kill()

            logging.info("CWD is %s %s", os.getcwd(), os.environ["AGENT_CWD"])

            agent_cwd = os.environ["AGENT_CWD"]

            logging.info("Killing workers")

            for worker in agent.workers:
                logging.info("Killing worker %s", worker)
                worker.kill()

            if os.path.exists(f"{agent_cwd}/agent.pid"):
                os.remove(f"{agent_cwd}/agent.pid")

            if os.path.exists(f"{agent_cwd}/worker.pid"):
                with open(f"{agent_cwd}/worker.pid", "r") as wfile:
                    workerpids = wfile.readlines()

                    for workerpid in workerpids:
                        workerpid = int(workerpid)
                        logging.info("Killing worker process %s", workerpid)
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

        logging.debug("[AgentShutdownPlugin] Startup Complete")

    def wait(self):
        pass

class AgentMonitorPlugin:

    def __init__(self):
        import sched
        import time

        logging.debug("[AgentMonitorPlugin] Creating")
        self.scheduler = sched.scheduler(time.time, time.sleep)

    @contextmanager
    def get_session(self):
        logging.debug("get_session: Creating session")
        engine = create_engine(CONFIG.get("database", "uri"))
        session = sessionmaker(bind=engine)()

        try:
            logging.debug("get_session: Yielding session")
            yield session
        except:
            logging.debug("get_session: Rollback session")
            session.rollback()
            raise
        else:
            logging.debug("get_session: Commit session")
            session.commit()
        finally:
            logging.debug("get_session: Closing session")
            session.close()

    def start(self, agent_service: AgentService):
        from billiard.context import Process
        logging.debug("[AgentMonitorPlugin] Starting")
        
        logging.debug("[AgentMonitorPlugin] Startup Complete")

        def monitor_processors():
            import sched

            processor_workers = []

            def main_loop(monitors, **kwargs):
                """ Main agent loop to monitor state of processors assigned to it and start, stop, pause, resume, kill them
                as their data objects change state. This includes managing the workers and deployments """

                logging.debug("[AgentMonitorPlugin] main_loop run %s %s", monitors, kwargs)
                logging.debug("[AgentMonitorPlugin] main_loop processors %s", processor_workers)

                process = psutil.Process(os.getpid())
                with self.get_session() as session:
                    logging.debug("[AgentMonitorPlugin] main_loop Worker memory before: %s",process.memory_info().rss)

                    # Get or create Agent
                    agent = (
                        session.query(AgentModel).filter_by(hostname=agent_service.name).first()
                    )

                    if agent is None:
                        agent = AgentModel(
                            hostname=agent_service.name, name=agent_service.name + ".agent", pid=os.getpid()
                        )

                    agent.pid = os.getpid()
                    agent.requested_status = "starting"
                    agent.status = "starting"

                    # Get or create Node for this agent
                    node = (
                        session.query(NodeModel).filter_by(hostname=agent.name).first()
                    )

                    if node is None:
                        node = NodeModel(
                            name=agent.name + ".node", agent=agent, hostname=agent.name
                        )
                        session.add(node)

                    agent.node = node
                
                    logging.info("[AgentMonitorPlugin] main_loop agent is %s",agent)
                    logging.info("[AgentMonitorPlugin] main_loop node is %s",node)
                    
                    logging.debug("[AgentMonitorPlugin] main_loop Worker memory after: %s",process.memory_info().rss)

                    # Get or create Node for this agent
                    _node = {}
                    # Get Processors for this agent
                    processors = []
                    # Get deployments for this host
                    deployments = []

                    [monitor.monitor(agent, processors, deployments, session=session) for monitor in monitors]

                    gc.collect()

                self.scheduler.enter(
                    3,
                    1,
                    main_loop,
                    argument=(monitors,),
                    kwargs=kwargs
                )

            # Create a list of pluggable "Monitor" objects that perform various independent tasks
            monitors = [ProcessorMonitor(), DeploymentMonitor(), NodeMonitor()]

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
        logging.debug("[PluginAgentService] Init")

    def start(self):

        os.environ["AGENT_CWD"] = os.getcwd()
        from datetime import datetime

        [plugin.start(self) for plugin in plugins]

        [plugin.wait() for plugin in plugins]