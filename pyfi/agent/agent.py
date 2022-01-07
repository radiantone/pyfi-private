"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import configparser
import glob
import logging
import multiprocessing
import os
import platform
import shutil
import signal
from contextlib import contextmanager
from pathlib import Path

import psutil
from flask import Flask

from pyfi.blueprints.show import blueprint
from pyfi.db.model import WorkerModel, AgentModel, NodeModel, DeploymentModel
from pyfi.worker import WorkerService

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

app.register_blueprint(blueprint)

HOME = str(Path.home())

CONFIG = configparser.ConfigParser()

global HOSTNAME
HOSTNAME: str = platform.node()

CPUS = multiprocessing.cpu_count()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]


def kill_containers():
    """Kill running containers"""
    import docker

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


# noinspection PyPep8
class AgentService:
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
        self.dburi = dburi
        self.node = None
        self.agent = None
        self.user = user
        self.size = size
        self.workerproc = None
        self.workerport = workerport
        self.name = name

        logging.info(f"Agent port is {port}")

        if name:
            global HOSTNAME
            HOSTNAME = name
            logging.info("Setting agent HOSTNAME to {}".format(name))

        if clean:
            logging.info("Cleaning work directories")
            if os.path.exists("work"):
                workdirs = glob.glob("work/*")

                for workdir in workdirs:
                    logging.info("Removing workdir %s", workdir)
                    shutil.rmtree(workdir)

        logging.info("Checking config at %s", HOME + "/pyfi.ini")
        if os.path.exists(HOME + "/pyfi.ini"):
            CONFIG.read(HOME + "/pyfi.ini")
            self.backend = CONFIG.get("backend", "uri")
            self.broker = CONFIG.get("broker", "uri")

    # noinspection PyPep8
    @contextmanager
    def get_session(self):
        session = self.database.session

        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

    def start(self):
        from datetime import datetime
        import bjoern
        from billiard.context import Process

        #########################################################################
        # Store my pid
        #########################################################################
        with open("agent.pid", "w") as procfile:
            procfile.write(str(os.getpid()))

        os.environ["AGENT_CWD"] = os.getcwd()

        logging.info(
            "Serving agent on port {} {} {}".format(
                self.port, self.backend, self.broker
            )
        )

        #########################################################################
        # Query or Create Agent
        #########################################################################
        agent = (
            self.database.session.query(AgentModel).filter_by(hostname=HOSTNAME).first()
        )

        if agent is None:
            # Create database ping process to notify pyfi that I'm here and active
            # agent process will monitor database and manage worker process pool
            # agent will report local available resources to database
            # agent will report # of active processors/CPUs and free CPUs
            agent = AgentModel(
                hostname=HOSTNAME, name=HOSTNAME + ".agent", pid=os.getpid()
            )

        agent.pid = os.getpid()
        agent.requested_status = "starting"
        agent.status = "starting"

        self.agent = agent
        #########################################################################

        vmem = psutil.virtual_memory()

        #########################################################################
        # Query or Create Node
        #########################################################################
        node = (
            self.database.session.query(NodeModel).filter_by(hostname=HOSTNAME).first()
        )

        if node is None:
            node = NodeModel(
                name=HOSTNAME + ".node", agent=self.agent, hostname=HOSTNAME
            )
            with self.get_session() as session:
                session.add(node)

            self.database.session.refresh(node)
        else:
            self.database.session.add(node)

        #########################################################################

        if node.agent is None:
            node.agent = agent


        #########################################################################
        # Set agent and node properties
        #########################################################################
        agent.node_id = node.id

        node.cpus = CPUS
        node.memsize = vmem.total
        node.freemem = vmem.free
        node.memused = vmem.percent
        self.node = node

        agent.status = "running"
        agent.cpus = CPUS
        agent.port = self.port
        agent.updated = datetime.now()

        with self.get_session() as session:
            session.add(agent)

        session.commit()

        #########################################################################
        # Shutdown agent
        #########################################################################
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

            logging.info("Killing worker")
            self.workerproc.kill()
            os.remove(f"{agent_cwd}/agent.pid")
            os.remove(f"{agent_cwd}/worker.pid")
            if os.path.exists(f"{agent_cwd}/worker.pid"):
                with open(f"{agent_cwd}/worker.pid", "r") as wfile:
                    workerpid = wfile.read()
                    workerpid = int(workerpid)
                    logging.info("Killing worker process %s", workerpid)
                    try:
                        os.killpg(os.getpgid(workerpid), 15)
                        os.kill(workerpid, signal.SIGKILL)
                    except Exception as ex:
                        logging.warning(ex)
            else:
                logging.warning("No worker.pid found")

            os.killpg(os.getpgid(os.getpid()), 15)
            os.kill(os.getpid(), signal.SIGKILL)
            process.kill()
            process.terminate()
            exit(0)

        signal.signal(signal.SIGINT, shutdown)

        #########################################################################
        # Monitor processors thread
        #########################################################################
        def monitor_processors():
            """
            Retrieve any processors that need compute resources, determine if you have free CPU's or idle workers,
            then create a worker with the processor's module and link the worker to the processor
            """
            import time

            processors = []
            workers = []

            def manage_processors(workers, processors):
                """
                Agents manage processors assigned to them and connect them to workers
                """
                from uuid import uuid4
                import psutil
                import shutil
                import os

                refresh = 0

                #########################################################################
                # Main Loop
                #########################################################################
                while True:

                    self.database.session.refresh(self.agent)

                    if self.agent.requested_status == "stop":
                        shutdown()

                    #########################################################################
                    # Resource conditions
                    #########################################################################
                    _vmem = psutil.virtual_memory()

                    self.node.memsize = _vmem.total
                    self.node.freemem = _vmem.free
                    self.node.memused = _vmem.percent

                    with self.get_session() as session:
                        session.add(self.node)

                    time.sleep(3)
                    sm = psutil.virtual_memory()
                    if sm.percent > 90.0:
                        # Send health alert log
                        logging.warning("VIRTUAL MEMORY > 90%")
                        for processor in processors:
                            if processor["worker"] is not None:
                                # Mark process last killed date and if it was killed
                                # a few times recently, then mark it stopped and save it
                                # adding a log.
                                processor["worker"]["process"].kill()
                                logging.warning("Setting worker to none")
                                processor["worker"] = None
                                processor["processor"].status = "stopped"

                    #########################################################################
                    # Check deployments for ones assigned to me
                    #########################################################################
                    mydeployments = []

                    # Gather host information and update node

                    if refresh == 0:
                        # Time to refresh all the processors from the
                        # TODO: Change to DeploymentModel
                        mydeployments = (
                            self.database.session.query(DeploymentModel)
                            .filter_by(hostname=HOSTNAME)
                            .all()
                        )

                        # Loop through existing processor references and refresh from database
                        # Check for moved processors
                        for processor in processors:
                            self.database.session.refresh(processor["processor"])

                            # Check if I already have a deployment
                            found = False
                            for deployment in mydeployments:
                                if deployment.processor == processor["processor"]:
                                    found = True
                                    break

                            agent_cwd = os.environ["AGENT_CWD"]
                            # If I have no deployment for the current processor, undeploy it
                            if not found:
                                logging.info("Processor no longer deployed")

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

                        # Loop through my database processors
                        for mydeployment in mydeployments:
                            myprocessor = mydeployment.processor
                            self.database.session.refresh(
                                myprocessor
                            )  # Might not be needed
                            if myprocessor.requested_status == "move":
                                continue

                            # If I don't already have this processor deployment
                            found = False
                            for processor in processors:
                                if processor["processor"].id == myprocessor.id:
                                    # If I already have it in my cache, update it
                                    processor["processor"] = myprocessor
                                    found = True

                            if not found:
                                # If this is a new processor, add it to cache
                                processors += [
                                    {"worker": None, "processor": myprocessor}
                                ]
                                logging.info("Added processor %s", myprocessor)

                    refresh += 1
                    if refresh >= 3:  # 3 cycle interval
                        refresh = 0

                    # Loop through my processor cache again and operate on them based
                    # on requested_status
                    for processor in processors:

                        logging.debug(
                            "Processor.requested_status START %s",
                            processor["processor"].requested_status,
                        )

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

                            with self.get_session() as session:
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
                                        "Killed worker %s", worker["worker"].id
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

                            with self.get_session() as session:
                                session.add(processor["deployment"].worker)
                                session.add(processor["processor"])

                        if processor["processor"].requested_status == "paused":
                            if processor["worker"] is not None:
                                logging.info("Pausing worker")
                                try:
                                    processor["worker"]["process"].suspend()
                                    logging.info(
                                        "Paused worker %s", worker["worker"].id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "paused"
                            processor["deployment"].worker.status = "paused"
                            processor["deployment"].worker.requested_status = "ready"

                            logging.info("Processor is paused")

                            with self.get_session() as session:
                                session.add(processor["deployment"].worker)
                                session.add(processor["processor"])

                            continue

                        if processor["processor"].requested_status == "resumed":
                            if processor["worker"] is not None:
                                logging.info("Resuming worker")
                                try:
                                    processor["worker"]["process"].resume()
                                    logging.info(
                                        "Paused worker %s", worker["worker"].id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "resumed"
                            processor["deployment"].worker.status = "resumed"
                            processor["deployment"].worker.requested_status = "ready"

                            logging.info("Processor is resumed")

                            with self.get_session() as session:
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
                                        "Killed worker %s", worker["worker"].id
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "stopped"
                            processor["deployment"].worker.status = "stopped"
                            processor["deployment"].worker.requested_status = "ready"

                            logging.info("Processor is stopped")

                            with self.get_session() as session:
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
                                logging.debug("process_died is %s", process_died)
                            except:
                                import traceback

                                print(traceback.format_exc())

                        if process_died:
                            logging.error("Process died!")

                        logging.debug("Process worker is %s", processor["worker"])

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

                            logging.debug("%s", process_died)
                            logging.debug("%s", processor["worker"])
                            logging.debug("%s", processor["processor"].requested_status)
                            logging.debug("%s", processor["processor"].status)

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
                                    self.database.session.query(WorkerModel)
                                    .filter_by(
                                        name=HOSTNAME
                                        + ".agent."
                                        + processor["processor"].name
                                        + ".worker"
                                    )
                                    .first()
                                )

                                if worker_model is None:
                                    logging.info("Creating worker model...")
                                    worker_model = WorkerModel(
                                        id=str(uuid4()),
                                        name=HOSTNAME
                                        + ".agent."
                                        + processor["processor"].name
                                        + ".worker",
                                        concurrency=processor["deployment"].cpus,
                                        status="ready",
                                        backend=self.backend,
                                        broker=self.broker,
                                        agent_id=self.agent.id,
                                        hostname=HOSTNAME,
                                        requested_status="start",
                                    )

                                processor["deployment"].worker = worker_model
                                worker_model.lastupdated = datetime.now()
                                worker_model.status = "running"
                                worker_model.processor = processor["processor"]

                                with self.get_session() as session:
                                    session.add(self.agent)
                                    session.add(worker_model)
                                    logging.info("Worker model is %s", worker_model)
                                    logging.info(
                                        "Agent worker is %s", self.agent.worker
                                    )
                                    self.agent.workers += [worker_model]

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
                                    "Agent: Creating Worker() queue size %s", self.size
                                )
                                print("%s", processor["processor"])

                                for deployment in processor["processor"].deployments:
                                    logging.info("Deployment worker %s", deployment)
                                    # Only launch worker if we have a deployment for our host
                                    if deployment.hostname == HOSTNAME:
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
                                            size=self.size,
                                            workdir=_dir,
                                            user=self.user,
                                            pool=self.pool,
                                            workerport=self.workerport,
                                            database=self.dburi,
                                            hostname=self.name,
                                            agent=agent,
                                            deployment=deployment,
                                            celeryconfig=self.config,
                                            backend=self.backend,
                                            broker=self.broker,
                                        )

                                        # = workerproc.worker_model
                                        # deployment.worker = workerproc.worker_model
                                        # deployment.worker.processor = processor['processor']
                                        # Setup the virtualenv only
                                        logging.info(
                                            f"-----------------------Starting {processor['processor'].name}"
                                        )
                                        workerproc.start(start=False)

                                        with self.get_session() as session:
                                            # session.add(workerproc.worker_model)
                                            worker_model = (
                                                session.query(WorkerModel)
                                                .filter_by(
                                                    name=HOSTNAME
                                                    + ".agent."
                                                    + processor["processor"].name
                                                    + ".worker"
                                                )
                                                .first()
                                            )
                                            # Launch from the virtualenv
                                            logging.info(
                                                f"-----------------------Launching {processor['processor'].name}"
                                            )
                                            wprocess = workerproc.launch(
                                                worker_model.name,
                                                agent.name,
                                                HOSTNAME,
                                                self.pool,
                                            )

                                            deployment.requested_status = "ready"
                                            deployment.status = "running"
                                            deployment.worker = worker_model
                                            # session.add(deployment.worker)
                                            deployment.worker.processor_id = processor[
                                                "processor"
                                            ].id
                                            deployment.worker.agent = self.agent

                                            logging.info(
                                                "-----------------------Worker process %s started.",
                                                wprocess.pid,
                                            )

                                            worker["worker"] = deployment.worker
                                            worker[
                                                "worker"
                                            ].process = workerproc.process.pid
                                            worker["process"] = workerproc
                                            worker["wprocess"] = wprocess

                                            processor["worker"] = worker
                                            logging.info(
                                                "-----------------------workerproc is %s",
                                                workerproc,
                                            )

                                            workers += [worker]

                                            logging.info(
                                                "-------------------------------------------------------"
                                            )

                            processor["processor"].requested_status = "ready"
                            processor["processor"].status = "running"

                            with self.get_session() as session:
                                session.add(processor["processor"])

            manage_processors(workers, processors)

        #########################################################################
        # Agent endpoints & health checks
        #########################################################################
        def web_server():
            from setproctitle import setproctitle

            try:
                setproctitle("pyfi agent::web_server")
                logging.info("Starting web server on %s", self.port)
                bjoern.run(app, "0.0.0.0", self.port)
            except Exception as ex:
                logging.error(ex)
                logging.info("web_server: exiting...")

        webserver = Process(target=web_server, daemon=True)
        webserver.start()

        logging.info("Monitoring processors")
        monitor_processors()


@app.route("/")
def hello():
    import json

    return json.dumps({"status": "green"})
