"""
Agent workerclass. Primary task/code execution context for processors. This is where all the magic happens
"""
import configparser
import inspect
import json
import logging

# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
import os
import platform
import shutil
import signal
import socket
import sys
import tracemalloc
from contextlib import closing
from inspect import Parameter
from multiprocessing import Condition, Process, Queue
from pathlib import Path
from typing import Type

import psutil
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from celery import Celery
from celery import chain as pipeline
from celery import current_app
from celery import group as parallel
from celery.signals import (
    setup_logging,
    task_failure,
    task_internal_error,
    task_postrun,
    task_prerun,
    task_received,
    task_success,
    worker_process_init,
)
from flask import Flask
from kombu import Exchange
from kombu import Queue as KQueue
from pytz import utc
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from pyfi.db import get_session
from pyfi.db.model import (
    AgentModel,
    CallModel,
    EventModel,
    PlugModel,
    ProcessorModel,
    SocketModel,
    UserModel,
    WorkerModel,
)
from pyfi.db.model.models import DeploymentModel

PRERUN_CONDITION = Condition()
POSTRUN_CONDITION = Condition()

app = Flask(__name__)

tracemalloc.start()


@setup_logging.connect
def setup_celery_logging(**kwargs):
    logging.debug("DISABLE LOGGING SETUP")


from celery.signals import setup_logging


@setup_logging.connect
def void(*args, **kwargs):
    """Override celery's logging setup to prevent it from altering our settings.
    github.com/celery/celery/issues/1867

    :return void:
    """
    pass


""" Prepare the module with some constants """
HOME = str(Path.home())
CONFIG = configparser.ConfigParser()

# Load the config
if os.path.exists(HOME + "/pyfi.ini"):
    CONFIG.read(HOME + "/pyfi.ini")
try:
    KEEP_WORKER_DIRS = CONFIG.get("worker", "keepdirs") == "true"
except:
    KEEP_WORKER_DIRS = False

DBURI = CONFIG.get("database", "uri")

# Create database engine
# , isolation_level='READ UNCOMMITTED'
DATABASE = create_engine(
    DBURI, pool_size=1, max_overflow=5, pool_recycle=3600, poolclass=QueuePool
)

events_server = os.environ["EVENTS"] if "EVENTS" in os.environ else "localhost"
lock = Condition()

QUEUE_SIZE = os.environ["PYFI_QUEUE_SIZE"] if "PYFI_QUEUE_SIZE" in os.environ else 10

global HOSTNAME
HOSTNAME = platform.node()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]


def fix(name):
    return name.replace(" ", ".")


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def execute_function(taskid, mname, fname, *args, **kwargs):
    """Executor for container based tasks"""
    import importlib
    import pickle

    with open("/tmp/" + taskid + ".log2", "w") as logs:
        logs.write("Importing module " + str(mname) + " " + str(fname))

    _args = args
    _kwargs = kwargs

    try:
        with open("/tmp/" + taskid + ".args", "rb") as argsfile:
            _args = pickle.load(argsfile)
    except:
        with open("/tmp/" + taskid + ".error", "w") as errorfile:
            errorfile.write("error")

    try:
        with open("/tmp/" + taskid + ".kwargs", "rb") as kwargsfile:
            _kwargs = pickle.load(kwargsfile)
    except:
        with open("/tmp/" + taskid + ".error", "w") as errorfile:
            errorfile.write("error")

    try:
        _module = importlib.import_module(str(mname))
        _function = getattr(_module, str(fname))
    except:
        with open("/tmp/" + taskid + ".error", "w") as errorfile:
            errorfile.write("error importing")

    result = _function(*_args, **_kwargs)

    with open("/tmp/" + taskid + ".out", "wb") as rfile:
        pickle.dump(result, rfile)

    return result


def shutdown(*args):
    """Shutdown worker"""
    from psutil import Process

    logging.debug("Shutting down...")
    process = Process(os.getpid())

    for child in process.children(recursive=True):
        logging.debug(
            "SHUTDOWN: Process pid {}: Killing child {}".format(process.pid, child.pid)
        )
        child.kill()

    process.kill()
    process.terminate()

    exit(0)


signal.signal(signal.SIGINT, shutdown)

run_times = {}


def dispatcher(processorid, plugid, message, socketid, **kwargs):
    """Execute a task based on a schedule"""
    backend = CONFIG.get("backend", "uri")
    broker = CONFIG.get("broker", "uri")

    # TODO: Figure out how to refresh processor, plug

    with get_session() as session:
        processor = session.query(ProcessorModel).filter_by(id=processorid).first()
        plug = session.query(PlugModel).filter_by(id=plugid).first()
        socket = session.query(SocketModel).filter_by(id=socketid).first()
        logging.debug("Dispatching %s PLUG %s", socket, plug)

        celery = Celery(backend=backend, broker=broker, include=processor.module)
        logging.debug("TASK NAMES: %s", celery.tasks.keys())
        try:
            name = plug.name

            if plug is None:
                logging.warning("Plug %s does not exist", name)
                return

            logging.debug("PLUG RESULT %s", plug is not None)

            # TODO: QUEUENAME
            tkey = (
                socket.queue.name + "." + fix(processor.name) + "." + socket.task.name
            )
            tkey = processor.module + "." + socket.task.name
            # tkey = socket.queue.name
            logging.debug("dispatcher: processor %s", processor.name)
            logging.debug("dispatcher: plug %s", plug.name)
            logging.debug(
                "dispatcher: plug: source %s:%s",
                plug.source.processor.name,
                plug.source.task.name,
            )
            logging.debug(
                "dispatcher: plug: target %s:%s",
                plug.target.processor.name,
                plug.target.task.name,
            )
            logging.debug("dispatcher: tkey %s", tkey)
            logging.debug("dispatcher: exchange %s", socket.queue.name)
            logging.debug("dispatcher: routing_key %s", tkey)

            queue = KQueue(
                tkey,
                Exchange(socket.queue.name, type="direct"),
                routing_key=tkey,
                message_ttl=plug.target.queue.message_ttl,
                durable=plug.target.queue.durable,
                expires=plug.target.queue.expires,
                # expires=30,
                # socket.queue.message_ttl
                # socket.queue.expires
                # TODO: These attributes need to come from Queue model
                queue_arguments={"x-message-ttl": 30000, "x-expires": 300},
            )

            logging.debug("Plug.argument %s", plug.argument)
            if plug.argument:
                logging.debug(
                    "Processor plug %s is connected to argument: %s",
                    plug,
                    plug.argument,
                )
                argument = {
                    "name": plug.argument.name,
                    "kind": plug.argument.kind,
                    "key": plug.target.processor.name
                    + "."
                    + plug.target.task.module
                    + "."
                    + plug.target.task.name,
                    "module": plug.target.task.module,
                    "function": plug.target.task.name,
                    "position": plug.argument.position,
                }

                logging.debug("Plug argument %s", plug.argument)
                kwargs["argument"] = argument
            else:
                logging.debug("Processor plug %s is not connected to argument.", plug)

            kwargs["function"] = socket.task.name

            task_sig = celery.signature(
                processor.module + "." + socket.task.name, queue=queue, kwargs=kwargs
            )

            delayed = task_sig.delay(message)

            logging.debug("dispatcher: Dispatched %s %s", task_sig, message)
        finally:
            pass


class TaskInvokeException(Exception):
    tb = None
    exception = None

    def __init__(self):
        super().__init__()


#########################################################################
# WorkerService class
#########################################################################
class WorkerService:
    """
    Worker wrapper that manages task ingress/egress and celery worker processes
    """

    container = None
    _session = None
    _connection = None

    def __init__(
        self,
        processor: Type[ProcessorModel],
        workdir: str,
        basedir: str,
        pool: int = 4,
        port: int = -1,
        size: int = 10,
        deployment: Type[DeploymentModel] = DeploymentModel,
        database=None,
        user: Type[UserModel] = UserModel,
        usecontainer: bool = False,
        skipvenv: bool = False,
        backend: str = "redis://localhost",
        hostname: str = None,
        agent: Type[AgentModel] = AgentModel,
        celeryconfig=None,
        broker: str = "pyamqp://localhost",
    ):
        """ """
        import multiprocessing

        global HOSTNAME

        self.backend = backend
        self.broker = broker
        self.port = port
        self.workdir = workdir
        self.dburi = database
        self.skipvenv = skipvenv
        self.usecontainer = usecontainer
        self.size = size
        self.basedir = basedir
        self.deploymentname = deployment.name
        self.agentname = agent.name
        self.processorid = processor.id
        self.worker_process = None
        self.data = {}

        if not self.port or self.port == -1:
            self.port = find_free_port()

        if os.path.isabs(self.workdir):
            self.workpath = self.workdir
            logging.debug("Setting workpath to %s", self.workpath)
        elif self.basedir.find(self.workdir) == -1:
            self.workpath = self.basedir + "/" + self.workdir
            logging.debug(
                "Setting workpath to basedir %s + workdir %s ",
                self.basedir,
                self.workdir,
            )
        else:
            self.workpath = self.basedir
            logging.debug("Setting workpath to %s", self.workpath)

        logging.debug("INIT WORKERSERVICE")

        if hostname:
            HOSTNAME = hostname
            self.hostname = hostname
            logging.debug("HOSTNAME is {}".format(hostname))
        else:
            hostname = HOSTNAME

        # Publish queue
        self.queue: Queue = Queue()

        # Main message database queue
        self.main_queue: Queue = Queue(self.size)

        # Received events
        self.received_queue: Queue = Queue()

        # Prerun events
        self.prerun_queue: Queue = Queue()

        # Postrun events
        self.postrun_queue: Queue = Queue()

        cpus = multiprocessing.cpu_count()

        with get_session() as session:

            _processor = (
                session.query(ProcessorModel).filter_by(id=self.processorid).first()
            )

            self.data = json.loads(str(_processor))
            """
            self.deployment = deployment = (
                session.query(DeploymentModel).filter_by(name=deployment.name).first()
            )
            self.worker = deployment.worker
            """
            agent = session.query(AgentModel).filter_by(name=agent.name).first()

            setattr(deployment, "status", "running")

            self.pool = pool
            self.user = user
            os.chdir(self.basedir)

            logging.debug("New Worker init: %s", processor.name)

            if os.path.exists(HOME + "/pyfi.ini"):
                CONFIG.read(HOME + "/pyfi.ini")
                self.backend = CONFIG.get("backend", "uri")
                self.broker = CONFIG.get("broker", "uri")

                """
                jobstores = {
                    'default': SQLAlchemyJobStore(url=CONFIG.get('database', 'uri'), metadata=Base.metadata, tablename=processor.name+'_jobs')
                }
                executors = {
                    "default": ThreadPoolExecutor(20),
                    "processpool": ProcessPoolExecutor(5),
                }
                """
                job_defaults = {"coalesce": False, "max_instances": 3}

                self.scheduler = BackgroundScheduler(
                    job_defaults=job_defaults, timezone=utc
                )
                from typing import Any, Dict

                self.jobs: Dict[str, Any] = {}

                logging.debug("JOBS %s", self.jobs)

                self.scheduler.print_jobs()

            if celeryconfig is not None:
                logging.debug("Applying celeryconfig from %s", celeryconfig)
                import importlib

                module = importlib.import_module(celeryconfig.split["."][:-1])
                celeryconfig = getattr(module, celeryconfig.split["."][-1:])
                self.celery = Celery(include=_processor.module)
                self.celery.config_from_object(celeryconfig)

            else:
                self.celery = Celery("pyfi", backend=backend, broker=broker)

                from pyfi.util import config

                logging.debug("App config is %s", config)
                self.celery.config_from_object(config)

            @self.celery.task(name=_processor.name + ".pyfi.celery.tasks.enqueue")
            def enqueue(data, *args, **kwargs):
                logging.debug("ENQUEUE: %s", data)
                return data

            logging.debug("Retrieving deployment by name %s", deployment.name)
            _deployment = (
                session.query(DeploymentModel).filter_by(name=deployment.name).first()
            )

            workerModel = self.workerModel = (
                session.query(WorkerModel)
                .filter_by(name=hostname + _processor.name + ".worker")
                .first()
            )
            workers = session.query(WorkerModel).filter_by(hostname=hostname).all()

            logging.debug("Found worker {}".format(workerModel))

            workerModel = None

            for worker in workers:
                if worker.deployment and worker.deployment.name == _deployment.name:
                    workerModel = worker
                    break

            if workerModel is not None:
                logging.debug("Worker deployment is {}".format(workerModel.deployment))
                logging.debug("Found %s workers for %s", len(workers), hostname)

            if workerModel is None:
                logging.debug("Creating new worker for %s", _deployment)
                workerModel = self.workerModel = WorkerModel(
                    name=HOSTNAME
                    + _processor.name
                    + ".worker."
                    + str(len(workers) + 1),
                    concurrency=int(_deployment.cpus),
                    status="ready",
                    backend=self.backend,
                    broker=self.broker,
                    processor=_processor,
                    agent_id=agent.id,
                    deployment=_deployment,
                    workerdir=self.workpath,
                    hostname=HOSTNAME,
                    requested_status="start",
                )

                logging.debug("Created workerModel")

                if not workerModel.agent_id:
                    workerModel.agent_id = agent.id

                session.add(workerModel)
                logging.debug("Added workerModel to session %s", workerModel)
                session.commit()

                workerModel.workerdir = self.workpath
                workerModel.port = self.port

                workerModel.deployment = _deployment
                _deployment.worker = workerModel
                _deployment.worker.processor = _processor
                logging.debug("Refreshing processor")
                logging.debug("Attached worker: Done")

        self.process = None
        logging.debug(
            "Starting worker with pool[{}] backend:{} broker:{}".format(
                pool, backend, broker
            )
        )

    #########################################################################
    # Launch worker in new shell
    #########################################################################
    def launch(self, name, agent, hostname, size):
        from subprocess import Popen

        """
        This method is used by the agent after the Worker() has been created and configured its venv.
        It is then launched using a subprocess running from that virtualenv
        The 'pyfi worker start' command will itself, run the start() method below.

        workerproc = Popen(["venv/bin/pyfi","worker","start","-n",processor['processor'].worker.name])
        """
        logging.debug("WORKER LAUNCH DIR is %s", os.getcwd())

        if os.path.exists("git"):
            logging.debug("Changing to git directory")
            os.chdir("git")

        process = None
        flow_cmd = "venv/bin/flow"

        if "FLOW_CMD" in os.environ:
            flow_cmd = os.environ["FLOW_CMD"]

        if not self.usecontainer:
            cmd = [
                flow_cmd,
                "worker",
                "start",
                "-s",
                "-n",
                name,
                "-h",
                hostname,
                "-a",
                agent,
                "-q",
                str(size),
            ]
            if self.user:
                cmd = [
                    flow_cmd,
                    "worker",
                    "start",
                    "-s",
                    "-n",
                    name,
                    "-h",
                    hostname,
                    "-a",
                    agent,
                    "-q",
                    str(size),
                ]

            cmd_str = " ".join(cmd)
            try:
                logging.info("Launching worker %s %s", cmd_str, name)
                dir = os.getcwd()

                if os.path.exists(flow_cmd):
                    self.process = process = Popen(
                        cmd,
                        stdout=sys.stdout,
                        stderr=sys.stdout,
                        preexec_fn=os.setsid,
                        cwd=dir,
                    )

                    with open(self.basedir + "/worker.pid", "a") as pidfile:
                        pidfile.write(str(process.pid))

                    logging.debug(
                        "Worker launched successfully: process %s.", self.process.pid
                    )
                else:
                    logging.debug("Worker packages not yet installed. Skipping launch")
            except:
                import traceback

                print(traceback.format_exc())
                pass
        else:
            """Run agent worker inside new or previously launched container"""
            raise NotImplementedError

        return process

    #########################################################################
    # Start worker thread
    #########################################################################
    def start(self, start=True, listen=True):
        """
        Worker start method
        """
        import json
        import os
        import time
        from threading import Thread

        def do_work():
            # Retrieve workmodels where worker=me and execute them
            pass

        """ Manage database interactions and task lifecycle messages """

        ################################################################
        def database_actions():
            """Main database interaction thread. Receives signals off a queue
            and conducts database operations based on the message"""
            from datetime import datetime
            from uuid import uuid4

            from pymongo import MongoClient

            mongoclient = MongoClient(CONFIG.get("mongodb", "uri"))
            redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

            logging.debug("database_actions: Starting...")
            with get_session() as session:
                while True:
                    logging.debug("database_actions: loop")
                    logging.debug("database_actions: Getting processor")
                    processor = (
                        session.query(ProcessorModel)
                        .filter_by(id=self.processorid)
                        .first()
                    )
                    logging.debug("database_actions: Got processor %s", processor.name)
                    # snapshot=tracemalloc.take_snapshot()
                    # for i, stat in enumerate(snapshot.statistics('filename')[:5], 1):
                    #    logging.debug("top_current %s %s", i, stat)

                    # session.refresh(processor)
                    # Check if any work has been assigned to me and then do it
                    # This will pause the task execution for this worker until the
                    # work is complete
                    do_work()

                    _plugs = {}

                    logging.debug("DBACTION: Processor %s", processor)
                    logging.debug(
                        "Checking main_queue[%s] with %s items",
                        self.size,
                        self.main_queue.qsize(),
                    )
                    logging.debug("---")
                    logging.debug("database_actions: Waiting on main_queue")
                    _signal = self.main_queue.get()
                    logging.debug(
                        "database_actions: main_queue: Got messages %s", _signal
                    )
                    logging.debug("---")
                    logging.debug("SIGNAL: %s", _signal)

                    if _signal["signal"] == "received":
                        try:
                            logging.debug("RECEIVED SIGNAL %s", _signal)

                            for _socket in processor.sockets:
                                logging.debug(
                                    "database_actions: Checking sender %s for task %s",
                                    _signal["sender"],
                                    _socket.task.name,
                                )
                                if _socket.task.name == _signal["sender"]:
                                    logging.debug(
                                        "RECEIVED SIGNAL: FOUND TASK %s", _socket.task
                                    )
                                    parent = None

                                    received = datetime.now()
                                    logging.debug("Found socket: %s", _socket)

                                    if "parent" not in _signal["kwargs"]:
                                        _signal["kwargs"]["parent"] = str(uuid4())
                                        logging.debug(
                                            "NEW PARENT %s", _signal["kwargs"]["parent"]
                                        )
                                        _signal["kwargs"][_socket.task.id] = []
                                        myid = _signal["kwargs"]["parent"]
                                    else:
                                        parent = _signal["kwargs"]["parent"]
                                        myid = str(uuid4())

                                    _signal["kwargs"]["myid"] = myid
                                    # For next call
                                    _signal["kwargs"]["parent"] = myid

                                    if "tracking" not in _signal["kwargs"]:
                                        _signal["kwargs"]["tracking"] = str(uuid4())

                                    _signal["kwargs"]["received"] = str(received)
                                    processor_path = (
                                        _socket.queue.name
                                        + "."
                                        + processor.name.replace(" ", ".")
                                    )

                                    _data = [
                                        "roomsg",
                                        {
                                            "channel": "task",
                                            "state": "received",
                                            "task": _socket.task.name,
                                            "module": _socket.task.module,
                                            "date": str(received),
                                            "room": processor.name,
                                        },
                                    ]

                                    # self.queue.put(_data)

                                    call = CallModel(
                                        id=myid,
                                        name=processor.module + "." + _socket.task.name,
                                        taskparent=_signal["taskparent"],
                                        socket=_socket,
                                        parent=parent,
                                        tracking=_signal["kwargs"]["tracking"],
                                        resultid="celery-task-meta-"
                                        + _signal["taskid"],
                                        celeryid=_signal["taskid"],
                                        task_id=_socket.task.id,
                                        state="received",
                                    )

                                    session.add(call)
                                    event = EventModel(
                                        name="received",
                                        note="Received task "
                                        + processor.module
                                        + "."
                                        + _socket.task.name,
                                    )

                                    session.add(event)
                                    call.events += [event]

                                    processor.requested_status = "ready"
                                    session.commit()
                                    logging.debug(
                                        "CREATED CALL %s %s", myid, _signal["taskid"]
                                    )

                                    self.queue.put(_data)
                                    logging.debug(
                                        "database_actions: Replying to received_queued %s",
                                        _signal["kwargs"],
                                    )
                                    self.received_queue.put(_signal["kwargs"])
                        except:
                            import traceback

                            print(traceback.format_exc())

                    if _signal["signal"] == "prerun":
                        logging.debug("Task PRERUN: %s", _signal)

                        for _socket in processor.sockets:
                            if _socket.task.name == _signal["sender"]:

                                parent = None

                                started = datetime.now()
                                if "parent" not in _signal["kwargs"]:
                                    _signal["kwargs"]["parent"] = str(uuid4())
                                    logging.debug(
                                        "NEW PARENT %s", _signal["kwargs"]["parent"]
                                    )
                                    _signal["kwargs"][_socket.task.id] = []
                                    myid = _signal["kwargs"]["parent"]
                                else:
                                    parent = _signal["kwargs"]["parent"]

                                processor_path = (
                                    _socket.queue.name
                                    + "."
                                    + processor.name.replace(" ", ".")
                                )

                                _data = [
                                    "roomsg",
                                    {
                                        "channel": "task",
                                        "state": "running",
                                        "task": _socket.task.name,
                                        "module": _socket.task.module,
                                        "date": str(started),
                                        "room": processor.name,
                                    },
                                ]

                                self.queue.put(_data)

                                sourceplug = None
                                logging.debug(
                                    "SOCKET TARGET PLUGS %s", _socket.sourceplugs
                                )

                                # TODO: Still needed?
                                for source in _socket.sourceplugs:
                                    logging.debug(
                                        "SOCKET QUEUE IS %s, SOURCE QUEUE is %s",
                                        _socket.queue.name,
                                        source.queue.name,
                                    )
                                    if source.queue.name == _socket.queue.name:
                                        sourceplug = source
                                        break

                                logging.debug("Looking up call %s", _signal["taskid"])
                                call = (
                                    session.query(CallModel)
                                    .filter_by(celeryid=_signal["taskid"])
                                    .first()
                                )

                                if call is None:
                                    logging.debug("Sleeping 1...")
                                    time.sleep(1)

                                    logging.debug(
                                        "Looking up call 2 %s ", _signal["taskid"]
                                    )
                                    call = (
                                        session.query(CallModel)
                                        .filter_by(celeryid=_signal["taskid"])
                                        .first()
                                    )

                                if call is not None:

                                    call.parent = parent
                                    _signal["kwargs"]["myid"] = call.id
                                    _signal["kwargs"]["parent"] = call.id

                                    logging.debug("RETRIEVED CALL %s", call)

                                    event = EventModel(
                                        name="prerun",
                                        note="Prerun for task "
                                        + processor.module
                                        + "."
                                        + _socket.task.name,
                                    )
                                    call.tracking = _signal["kwargs"]["tracking"]
                                    session.add(event)
                                    call.events += [event]
                                    session.add(call.socket)
                                    session.add(call)
                                    session.commit()
                                else:
                                    logging.warning(
                                        "No Call found with celeryid=[%s]",
                                        _signal["taskid"],
                                    )
                                    # log error event
                                    session.rollback()

                                _signal["kwargs"]["plugs"] = _plugs
                                logging.debug(
                                    "Putting %s on PRERUN_QUEUE", _signal["kwargs"]
                                )
                                self.prerun_queue.put(_signal["kwargs"])
                                logging.debug(
                                    "Done Putting %s on PRERUN_QUEUE", _signal["kwargs"]
                                )

                    if _signal["signal"] == "postrun":
                        """
                        Task has completed, now we need to determine how to send the results to downstream plugs
                        """
                        import json
                        import pickle
                        from datetime import datetime
                        from urllib.parse import urlparse

                        from rejson import Client, Path

                        logging.debug("POSTRUN: SIGNAL: %s", _signal)
                        logging.debug("POSTRUN: KWARGS: %s", _signal["kwargs"])
                        task_kwargs = _signal["kwargs"]
                        plugs = task_kwargs["plugs"]

                        pass_kwargs = {}

                        if "tracking" in task_kwargs:
                            pass_kwargs["tracking"] = task_kwargs["tracking"]
                        if "parent" in task_kwargs:
                            pass_kwargs["parent"] = task_kwargs["parent"]
                            logging.debug("SETTING PARENT: %s", pass_kwargs)

                        myid = task_kwargs["myid"]
                        pass_kwargs["postrun"] = str(datetime.now())

                        try:
                            # Is there a call already associated with this task? There should be!
                            call = session.query(CallModel).filter_by(id=myid).first()

                            logging.debug("CALL QUERY %s", call)

                            # Add postrun event to the call
                            if call:
                                if "argument" in _signal["kwargs"]:
                                    call.argument = _signal["kwargs"]["argument"][
                                        "name"
                                    ]

                                call.finished = datetime.now()
                                call.state = "finished"
                                event = EventModel(
                                    name="postrun", note="Postrun for task"
                                )
                                rb = redisclient.get(call.resultid)
                                rbjson = pickle.loads(rb)
                                logging.info(
                                    "database_actions: rb result %s %s",
                                    call.resultid,
                                    rbjson,
                                )
                                celery_db = mongoclient["celery"]

                                insert_res = celery_db.celery_taskmeta.insert_one(
                                    rbjson
                                )
                                logging.debug(
                                    "database_actions: insert_res %s", insert_res
                                )

                                session.add(event)
                                call.events += [event]
                                session.add(call)
                                session.commit()
                            else:
                                logging.warning(
                                    "No pre-existing Call object for id %s", myid
                                )
                        except:
                            import traceback

                            print(traceback.format_exc())
                            logging.error("No pre-existing Call object for id %s", myid)

                        sourceplugs = {}
                        data = {
                            "module": processor.module,
                            "date": str(datetime.now()),
                            "resultkey": "celery-task-meta-" + _signal["taskid"],
                            "message": "Processor message",
                            "channel": "task",
                            "room": processor.name,
                            "task": _signal["sender"],
                        }

                        # Dispatch result to connected plugs
                        for _socket in processor.sockets:

                            # Find the socket associated with this task
                            if _socket.task.name == _signal["sender"]:

                                for plug in _socket.sourceplugs:
                                    _plugs[plug.name] = []
                                    sourceplugs[plug.name] = plug

                                # Build path to the task
                                processor_path = (
                                    _socket.queue.name
                                    + "."
                                    + processor.name.replace(" ", ".")
                                )

                                # Create data record for this event
                                data = {
                                    "module": processor.module,
                                    "date": str(datetime.now()),
                                    "resultkey": "celery-task-meta-"
                                    + _signal["taskid"],
                                    "message": "Processor message",
                                    "channel": "task",
                                    "room": processor.name,
                                    "task": _signal["sender"],
                                }

                                payload = json.dumps(data)
                                logging.debug("postrun: payload %s", data)
                                data["message"] = payload
                                break

                        # Add task result to data record
                        _r = _signal["result"]
                        logging.debug("RESULT2: %s %s", type(_r), _r)
                        try:
                            result = json.dumps(_r, indent=4)
                        except:
                            result = str(_r)

                        data["duration"] = _signal["duration"]
                        data["message"] = json.dumps(result)
                        data["message"] = json.dumps(data)
                        data["error"] = False

                        logging.debug("REDIS JSON: Connecting to %s", self.backend)
                        rj = Client(
                            host=urlparse(CONFIG.get("redis", "uri")).hostname,
                            port=6379,
                            decode_responses=True,
                        )
                        rj.jsonset(
                            "celery-task-result-" + _signal["taskid"],
                            Path.rootPath(),
                            _r,
                        )
                        logging.debug(
                            "REDIS JSON:%s %s",
                            "celery-task-result-" + _signal["taskid"],
                            _r,
                        )
                        logging.debug("postrun: result: %s", result)
                        if isinstance(_r, TaskInvokeException):
                            data["error"] = True
                            data["message"] = _r.tb

                        data["state"] = "postrun"

                        logging.debug("DATA2: %s", data)
                        logging.debug("EMITTING ROOMSG: %s", data)

                        # Put data record into queue for emission
                        self.queue.put(["roomsg", data])

                        # Put log event into queue for emission
                        self.queue.put(
                            [
                                "roomsg",
                                {
                                    "channel": "log",
                                    "date": str(datetime.now()),
                                    "room": processor.name,
                                    "message": "A log message!",
                                },
                            ]
                        )

                        logging.debug("PLUGS-: %s", plugs)

                        pipelines = []

                        for pname in sourceplugs:
                            logging.debug("PLUG Pname: %s", pname)
                            processor_plug = None

                            if pname not in sourceplugs:
                                logging.warning("%s plug not in %s", pname, sourceplugs)
                                continue

                            processor_plug = sourceplugs[pname]

                            if data["error"] and processor_plug.type != "ERROR":
                                logging.debug(
                                    "Skipping non-error processor plug {} for data error {}".format(
                                        processor_plug, data
                                    )
                                )
                                continue

                            logging.debug("postrun: Using PLUG: %s", processor_plug)

                            if processor_plug is None:
                                logging.warning(
                                    "No plug named [%s] found for processor[%s]",
                                    pname,
                                    processor.name,
                                )
                                continue

                            logging.debug("postrun: Querying target processor")
                            target_processor = (
                                session.query(ProcessorModel)
                                .filter_by(id=processor_plug.target.processor_id)
                                .first()
                            )

                            msgs = [(result, _r)]

                            logging.debug("msgs %s", msgs)

                            """
                            NOTE: Maybe the logic here is for the plug to have its own queue and to invoke an internal
                            task on that queue. The task accepts the metadata to invoke the actual socket function.
                            This would result in the plug queue having its own statistics separate from the socket queue
                            """

                            """
                            NOTE: Create a pipeline that invokes the plug queue with internal "plug_task" task, then add
                            this signature for the socket after that. BINGO! Now we can track individual queues for each plug
                            that have their own properties and they will stack up before the actual socket task is called.
                            # For each plug add to a parallel then run as a single task

                            plugqueue = KQueue(,....,...,processor_plug.queue.name,....)     # e.g. pyfi.queue2
                            parallel(
                                pipeline(
                                    signature('pyfi.celery.tasks.enqueue', plugqueue, .....),    # Pass data through
                                    self.celery.signature(
                                        target_processor.module+'.'+processor_plug.target.task.name, args=(msg,), queue=worker_queue, kwargs=pass_kwargs).delay()
                                ),
                                pipeline(
                                    signature('pyfi.celery.tasks.enqueue', plugqueue, .....),    # Pass data through
                                    self.celery.signature(
                                        target_processor.module+'.'+processor_plug.target.task.name, args=(msg,), queue=worker_queue, kwargs=pass_kwargs).delay()
                                )
                            )
                            """
                            for msg, _result in msgs:
                                """We have data in an outbound queue and need to find the associated plug and socket to construct the call
                                and pass the data along"""

                                if hasattr(
                                    _result, "plugs"
                                ) and processor_plug.name not in list(
                                    getattr(_result, "plugs")
                                ):
                                    # This result is select
                                    continue
                                elif hasattr(
                                    _result, "plugs"
                                ) and processor_plug.name in list(
                                    getattr(_result, "plugs")
                                ):
                                    # Pull the result object out
                                    msg = getattr(_result, "result")
                                    try:
                                        msg = json.dumps(msg, indent=4)
                                    except:
                                        msg = str(msg)

                                key = processor_plug.target.queue.name
                                # TODO: QUEUENAME Should this just be key?
                                tkey = (
                                    key
                                    + "."
                                    + fix(target_processor.name)
                                    + "."
                                    + processor_plug.target.task.name
                                )

                                logging.debug("postrun: tkey %s", tkey)
                                tkey2 = key + "." + processor_plug.target.task.name

                                logging.debug(
                                    "Sending {} to queue {}".format(msg, tkey)
                                )

                                if processor_plug.target.queue.qtype == "direct":
                                    logging.debug("Finding processor....")

                                    socket = processor_plug.target

                                    logging.debug(
                                        "Invoking {}=>{}({})".format(
                                            key,
                                            target_processor.module
                                            + "."
                                            + processor_plug.target.task.name,
                                            msg,
                                        )
                                    )

                                    plug_queue = KQueue(
                                        processor_plug.queue.name,
                                        Exchange(
                                            processor_plug.queue.name, type="direct"
                                        ),
                                        routing_key=fix(processor.name)
                                        + ".pyfi.celery.tasks.enqueue",
                                        message_ttl=processor_plug.queue.message_ttl,
                                        durable=processor_plug.queue.durable,
                                        expires=processor_plug.queue.expires,
                                        # expires=30,
                                        # socket.queue.message_ttl
                                        # socket.queue.expires
                                        # TODO: These attributes need to come from Queue model
                                        queue_arguments={
                                            "x-message-ttl": 30000,
                                            "x-expires": 300,
                                        },
                                    )

                                    logging.debug(
                                        "postrun: built plug queue %s", plug_queue
                                    )
                                    # TODO: Task queue
                                    plug_sig = self.celery.signature(
                                        processor.name + ".pyfi.celery.tasks.enqueue",
                                        args=(msg,),
                                        queue=plug_queue,
                                        kwargs=pass_kwargs,
                                    )

                                    plug_queue = KQueue(
                                        processor_plug.queue.name,
                                        Exchange(
                                            processor_plug.queue.name, type="direct"
                                        ),
                                        routing_key=tkey,
                                        message_ttl=processor_plug.queue.message_ttl,
                                        durable=processor_plug.queue.durable,
                                        expires=processor_plug.queue.expires,
                                        # expires=30,
                                        # socket.queue.message_ttl
                                        # socket.queue.expires
                                        # TODO: These attributes need to come from Queue model
                                        # processor_plug.queue.ttl etc
                                        queue_arguments={
                                            "x-message-ttl": 30000,
                                            "x-expires": 300,
                                        },
                                    )
                                    # Declare worker queue using target queue properties
                                    worker_queue = KQueue(
                                        tkey,
                                        Exchange(key, type="direct"),
                                        routing_key=tkey,
                                        message_ttl=processor_plug.target.queue.message_ttl,
                                        durable=processor_plug.target.queue.durable,
                                        expires=processor_plug.target.queue.expires,
                                        # expires=30,
                                        # socket.queue.message_ttl
                                        # socket.queue.expires
                                        # TODO: These attributes need to come from Queue model
                                        queue_arguments={
                                            "x-message-ttl": 30000,
                                            "x-expires": 300,
                                        },
                                    )

                                    task_queue = KQueue(
                                        tkey2,
                                        Exchange(key, type="direct"),
                                        routing_key=tkey2,
                                        message_ttl=processor_plug.target.queue.message_ttl,
                                        durable=processor_plug.target.queue.durable,
                                        expires=processor_plug.target.queue.expires,
                                        # expires=30,
                                        # socket.queue.message_ttl
                                        # socket.queue.expires
                                        # TODO: These attributes need to come from Queue model
                                        queue_arguments={
                                            "x-message-ttl": 30000,
                                            "x-expires": 300,
                                        },
                                    )

                                    logging.debug("worker queue %s", worker_queue)
                                    logging.debug("task queue %s", worker_queue)
                                    task_sig = None

                                    # Create task signature
                                    try:
                                        logging.debug("PASS_KWARGS: %s", pass_kwargs)

                                        if processor_plug.argument:
                                            logging.debug(
                                                "Processor plug is connected to argument: %s",
                                                processor_plug.argument,
                                            )
                                            argument = {
                                                "name": processor_plug.argument.name,
                                                "kind": processor_plug.argument.kind,
                                                "key": processor_plug.target.processor.name
                                                + "."
                                                + processor_plug.target.task.module
                                                + "."
                                                + processor_plug.target.task.name,
                                                "module": processor_plug.target.task.module,
                                                "function": processor_plug.target.task.name,
                                                "position": processor_plug.argument.position,
                                            }
                                            pass_kwargs["argument"] = argument
                                        else:
                                            logging.debug(
                                                "Processor plug not connected to argument."
                                            )

                                        plug_task_sig = (
                                            processor_plug.queue.name
                                            + "."
                                            + target_processor.module
                                            + "."
                                            + processor_plug.target.task.name
                                        )

                                        logging.debug(
                                            "postrun: plug_task_sig %s", plug_task_sig
                                        )
                                        # PLUG ROUTING
                                        task_sig = self.celery.signature(
                                            plug_task_sig,
                                            args=(msg,),
                                            # TODO: QUEUENAME
                                            # queue=plug_queue
                                            # This will ensure that each "edge" in the flow, which is one plug connecting
                                            # two sockets, has its own assigned queue for invoking the target task
                                            # queue=worker_queue,
                                            queue=plug_queue,
                                            kwargs=pass_kwargs,
                                        )
                                        """
                                        task_sig = self.celery.signature(
                                            target_processor.module
                                            + "."
                                            + processor_plug.target.task.name,
                                            args=(msg,),
                                            # TODO: QUEUENAME
                                            # queue=plug_queue
                                            # This will ensure that each "edge" in the flow, which is one plug connecting
                                            # two sockets, has its own assigned queue for invoking the target task
                                            #queue=worker_queue,
                                            queue=plug_queue,
                                            kwargs=pass_kwargs,
                                        )
                                        """
                                        delayed = pipeline(task_sig)
                                        pipelines += [delayed]
                                        logging.debug("   ADDED TASK SIG: %s", task_sig)
                                    except:
                                        import traceback

                                        print(traceback.format_exc())

                                    if task_sig:
                                        logging.debug(
                                            "call complete %s %s %s %s",
                                            processor_plug.queue.name
                                            + "."
                                            + target_processor.module
                                            + "."
                                            + processor_plug.target.task.name,
                                            (msg,),
                                            plug_queue,
                                            task_sig,
                                        )

                        logging.debug("postrun: delayed = parallel(*pipelines).delay()")
                        delayed = parallel(*pipelines).delay()
                        logging.debug("postrun: delayed %s", delayed)

        # Start database session thread. Provides a single thread and active session
        # to perform all database interactions. Receives messages from queue

        def start_database_actions():
            dbactions = Thread(target=database_actions)
            dbactions.start()
            logging.debug("database_actions started...")

        """ Main worker process/thread"""

        #################################
        def worker_proc(app, _queue, dburi):
            """Main celery worker thread. Configure worker, queues and launch celery worker"""
            import builtins
            import importlib
            import json
            import sys
            import time
            from uuid import uuid4

            from setproctitle import setproctitle

            import docker

            logging.info("Entering worker_proc")
            setproctitle("pyfi worker::worker_proc")

            job_defaults = {"coalesce": False, "max_instances": 3}

            scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=utc)

            queues = []

            with get_session() as session:
                myprocessor = (
                    session.query(ProcessorModel).filter_by(id=self.processorid).first()
                )
                deployment = (
                    session.query(DeploymentModel)
                    .filter_by(name=self.deploymentname)
                    .first()
                )
                agent = session.query(AgentModel).filter_by(name=self.agentname).first()

                logging.info("use_container %s", myprocessor.use_container)

                if myprocessor.use_container:
                    agent_cwd = os.environ["AGENT_CWD"]

                    client = docker.from_env()
                    logging.info(
                        "Worker: Checking processor.detached....%s",
                        myprocessor.detached,
                    )
                    if True:
                        logging.info(
                            "Running container %s:%s....",
                            myprocessor.container_image,
                            myprocessor.container_version,
                        )

                        if not os.path.exists("out"):
                            os.mkdir("out")
                        try:
                            self.container = client.containers.get(
                                HOSTNAME + "." + myprocessor.module
                            )
                        except Exception:
                            self.container = client.containers.run(
                                myprocessor.container_image
                                + ":"
                                + myprocessor.container_version,
                                auto_remove=True,
                                name=HOSTNAME + "." + myprocessor.module,
                                volumes={
                                    os.getcwd()
                                    + "/out": {"bind": "/tmp/", "mode": "rw"}
                                },
                                entrypoint="",
                                command="tail -f /etc/hosts",
                                detach=True,
                            )

                        # TODO: Create or Update ContainerModel
                        # Add ContainerModel to self.deployment.container

                        logging.info("Working starting container....%s", self.container)
                        logging.info(
                            "Container started %s:%s....%s",
                            myprocessor.container_image,
                            myprocessor.container_version,
                            self.container,
                        )

                        logging.info(
                            "Installing repo inside container...%s",
                            myprocessor.gitrepo.strip(),
                        )

                        # TODO: Only install repo if processor has one
                        # TODO: Install requirements.txt if processor has one
                        # Install the repo inside the container
                        res = self.container.exec_run(
                            "pip install -e git+" + myprocessor.gitrepo.strip()
                        )

                        logging.info("OUTPUT: %s", res.output)

                        with open(f"{agent_cwd}/{myprocessor.name}.pid", "w") as cfile:
                            cfile.write(str(self.container.short_id) + "\n")

                        with open(f"{agent_cwd}/containers.pid", "a") as cfile:
                            cfile.write(str(self.container.short_id) + "\n")
                        # Append container id to containers.pid

                logging.debug("Worker starting session....")

                logging.debug("Worker got session....")
                # session.refresh(myprocessor)
                logging.debug("================== WORKER PROCESSOR %s", myprocessor)
                logging.debug("Getting processor {}".format(myprocessor.id))
                task_queues = []
                task_routes = {}

                logging.debug("My processor is: {}".format(myprocessor))

                _processor = myprocessor

                session.commit()

                if _processor and _processor.sockets and len(_processor.sockets) > 0:
                    """Set up task routes"""
                    logging.debug("Setting up sockets...")
                    for _socket in _processor.sockets:
                        logging.debug("Socket %s", _socket)
                        if _socket.queue:

                            # TODO: Use socket.task.name as the task name and _processor.module as the module
                            # For each socket task, use a queue named socket.queue.name+_processor.name+socket.task.name
                            # for example: queue1.proc1.some_task_A, queue1.proc1.some_task_B

                            # This queue is bound to a broadcast(fanout) exchange that delivers
                            # a message to all the connected queues however sending a task to
                            # this queue will deliver to this processor only
                            processor_path = (
                                _socket.queue.name
                                + "."
                                + _processor.name.replace(" ", ".")
                            )

                            logging.debug("Joining room %s", processor_path)
                            if processor_path not in queues:
                                queues += [processor_path]

                            processor_task = (
                                _socket.queue.name
                                + "."
                                + _processor.name.replace(" ", ".")
                                + "."
                                + _socket.task.name
                            )
                            processor_task2 = (
                                _processor.module + "." + _socket.task.name
                            )

                            if processor_task not in queues:
                                # room = {'room': processor_task}
                                queues += [processor_task]

                            if processor_task2 not in queues:
                                queues += [processor_task2]

                            # This topic queue represents the broadcast fanout to all workers connected
                            # to it. Sending a task to this queue delivers to all connected workers
                            # queues += []

                            from kombu import Exchange, Queue

                            logging.debug(
                                "socket.queue.expires %s", _socket.queue.expires
                            )

                            for processor_plug in _socket.targetplugs:
                                """PLUG ROUTING"""
                                tkey = (
                                    processor_plug.source.queue.name
                                    + "."
                                    + _processor.module
                                    + "."
                                    + processor_plug.source.task.name
                                )
                                tkey2 = (
                                    _processor.module
                                    + "."
                                    + processor_plug.source.task.name
                                )

                                # PLUG ROUTING
                                routing_key = (
                                    processor_plug.queue.name
                                    + "."
                                    + _processor.module
                                    + "."
                                    + processor_plug.target.task.name
                                )

                                # PLUG ROUTING
                                plug_queue = KQueue(
                                    processor_plug.queue.name,
                                    Exchange(
                                        processor_plug.queue.name,
                                        type="direct",
                                    ),
                                    routing_key=routing_key,
                                    message_ttl=_socket.queue.message_ttl,
                                    durable=_socket.queue.durable,
                                    expires=_socket.queue.expires,
                                    # socket.queue.message_ttl
                                    # socket.queue.expires
                                    # TODO: These attributes need to come from Queue model
                                    queue_arguments={
                                        "x-message-ttl": 30000,
                                        "x-expires": 300,
                                    },
                                )
                                # PLUG ROUTING
                                task_routes[
                                    processor_plug.queue.name
                                    + "."
                                    + _processor.module
                                    + "."
                                    + _socket.task.name
                                ] = {
                                    "queue": processor_plug.queue.name,
                                    "exchange": [processor_plug.queue.name],
                                }

                                # PLUG ROUTING
                                logging.debug(
                                    "ADDED ROUTE %s for %s",
                                    processor_plug.queue.name
                                    + "."
                                    + _processor.module
                                    + "."
                                    + _socket.task.name,
                                    task_routes[
                                        processor_plug.queue.name
                                        + "."
                                        + _processor.module
                                        + "."
                                        + _socket.task.name
                                    ],
                                )
                                logging.debug("ADDED TARGET PLUG QUEUE %s", plug_queue)
                                task_queues += [plug_queue]

                            for processor_plug in _socket.sourceplugs:
                                """PLUG ROUTING"""
                                tkey = (
                                    processor_plug.target.queue.name
                                    + "."
                                    + fix(_processor.name)
                                    + "."
                                    + processor_plug.target.task.name
                                )
                                tkey2 = (
                                    _processor.module
                                    + "."
                                    + processor_plug.target.task.name
                                )

                                # PLUG ROUTING
                                routing_key = (
                                    processor_plug.target.queue.name
                                    + "."
                                    + fix(_processor.name)
                                    + "."
                                    + _socket.task.name
                                )

                                # PLUG ROUTING
                                plug_queue = KQueue(
                                    processor_plug.target.queue.name,
                                    Exchange(
                                        processor_plug.target.queue.name,
                                        type="direct",
                                    ),
                                    routing_key=routing_key,
                                    message_ttl=_socket.queue.message_ttl,
                                    durable=_socket.queue.durable,
                                    expires=_socket.queue.expires,
                                    # socket.queue.message_ttl
                                    # socket.queue.expires
                                    # TODO: These attributes need to come from Queue model
                                    queue_arguments={
                                        "x-message-ttl": 30000,
                                        "x-expires": 300,
                                    },
                                )

                                # PLUG ROUTING
                                task_routes[
                                    processor_plug.target.queue.name
                                    + "."
                                    + _processor.module
                                    + "."
                                    + _socket.task.name
                                ] = {
                                    "queue": processor_plug.target.queue.name,
                                    "exchange": [processor_plug.target.queue.name],
                                }

                                # PLUG ROUTING
                                logging.debug(
                                    "ADDED ROUTE %s for %s",
                                    processor_plug.target.queue.name
                                    + "."
                                    + _processor.module
                                    + "."
                                    + _socket.task.name,
                                    task_routes[
                                        processor_plug.target.queue.name
                                        + "."
                                        + _processor.module
                                        + "."
                                        + _socket.task.name
                                    ],
                                )
                                logging.debug("ADDED SOURCE PLUG QUEUE %s", plug_queue)
                                task_queues += [plug_queue]

                            task_queues += [
                                KQueue(
                                    _socket.queue.name
                                    + "."
                                    + fix(_processor.name)
                                    + "."
                                    + _socket.task.name,
                                    Exchange(
                                        _socket.queue.name
                                        + "."
                                        + fix(_processor.name)
                                        + "."
                                        + _socket.task.name,
                                        type="direct",
                                    ),
                                    routing_key=_socket.queue.name
                                    + "."
                                    + fix(_processor.name)
                                    + "."
                                    + _socket.task.name,
                                    message_ttl=_socket.queue.message_ttl,
                                    durable=_socket.queue.durable,
                                    expires=_socket.queue.expires,
                                    # socket.queue.message_ttl
                                    # socket.queue.expires
                                    # TODO: These attributes need to come from Queue model
                                    queue_arguments={
                                        "x-message-ttl": 30000,
                                        "x-expires": 300,
                                    },
                                )
                            ]

                            task_queues += [
                                KQueue(
                                    _processor.module + "." + _socket.task.name,
                                    Exchange(
                                        _socket.queue.name
                                        + "."
                                        + fix(_processor.name)
                                        + "."
                                        + _socket.task.name,
                                        type="direct",
                                    ),
                                    routing_key=_processor.module
                                    + "."
                                    + _socket.task.name,
                                    message_ttl=_socket.queue.message_ttl,
                                    durable=_socket.queue.durable,
                                    expires=_socket.queue.expires,
                                    # socket.queue.message_ttl
                                    # socket.queue.expires
                                    # TODO: These attributes need to come from Queue model
                                    queue_arguments={
                                        "x-message-ttl": 30000,
                                        "x-expires": 300,
                                    },
                                )
                            ]

                            task_queues += [
                                KQueue(
                                    _socket.queue.name
                                    + "."
                                    + fix(_processor.name)
                                    + "."
                                    + _socket.task.name,
                                    Exchange(
                                        _socket.queue.name + ".topic", type="fanout"
                                    ),
                                    routing_key=_socket.queue.name + ".topic",
                                    message_ttl=_socket.queue.message_ttl,
                                    durable=_socket.queue.durable,
                                    expires=_socket.queue.expires,
                                    # TODO: These attributes need to come from Queue model
                                    queue_arguments={
                                        "x-message-ttl": 30000,
                                        "x-expires": 300,
                                    },
                                )
                            ]

                            task_routes[_processor.module + "." + _socket.task.name] = {
                                "queue": _socket.queue.name,
                                "exchange": [
                                    _socket.queue.name + ".topic",
                                    _socket.queue.name,
                                ],
                            }
                            """
                            task_routes[self.processor.module + '.' + socket.task.name + '.wait'] = {
                                'queue': socket.queue.name,
                                'exchange': [socket.queue.name + '.' + self.processor.name.replace(
                                    ' ', '.') + '.' + socket.task.name, socket.queue.name]
                            }
                            """

                @worker_process_init.connect()
                def prep_db_pool(**kwargs):
                    """
                    When Celery fork's the parent process, the db engine & connection pool is included in that.
                    But, the db connections should not be shared across processes, so we tell the engine
                    to dispose of all existing connections, which will cause new ones to be opend in the child
                    processes as needed.
                    More info: https://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing
                    """
                    return

                app.conf.task_queues = task_queues
                app.conf.task_routes = task_routes
                logging.debug("TASK_ROUTES %s", task_routes.keys())
                logging.debug(
                    "Creating celery worker %s %s %s deployment %s",
                    _processor.name + "@" + HOSTNAME,
                    self.backend,
                    self.broker,
                    deployment.cpus,
                )

                """ Create celery worker """
                worker = None
                try:
                    worker = app.Worker(
                        hostname=self.hostname
                        + "."
                        + _processor.name
                        + "."
                        + deployment.name
                        + "@"
                        + agent.hostname,
                        backend=self.backend,
                        broker=self.broker,
                        beat=_processor.beat,
                        uid="pyfi",
                        without_mingle=True,
                        without_gossip=True,
                        concurrency=int(deployment.cpus),
                    )
                    worker.concurrency = int(deployment.cpus)
                except Exception as ex:
                    logging.error(ex)

                logging.debug("Created celery worker")

                logging.debug("TASK KEYS %s", current_app.tasks.keys())

                """ Find or create a WorkerModel for this worker """
                try:
                    logging.debug(
                        "Creating workerModel with worker dir %s", self.workpath
                    )

                    if deployment.worker:
                        workerModel = deployment.worker
                    else:
                        workerModel = (
                            session.query(WorkerModel)
                            .filter_by(name=HOSTNAME + _processor.name + ".worker")
                            .first()
                        )

                    if workerModel is None:
                        workerModel = WorkerModel(
                            name=HOSTNAME + _processor.name + ".worker",
                            concurrency=int(deployment.cpus),
                            status="ready",
                            backend=self.backend,
                            processor=_processor,
                            broker=self.broker,
                            workerdir=self.workpath,
                            agent_id=agent.id,
                            hostname=HOSTNAME,
                            port=self.port,
                            requested_status="start",
                        )

                        logging.debug("Created workerModel")
                        session.add(workerModel)

                    workerModel.workerdir = self.workpath

                    """ Attach worker to deployment """
                    deployment.worker = workerModel
                    deployment.worker.hostname = HOSTNAME
                    workerModel.deployment = deployment
                    workerModel.port = self.port
                    session.commit()
                except Exception as ex:
                    logging.error(ex)

                logging.debug("Checking beat")
                if _processor.beat:
                    logging.debug("Has beat")
                    worker.app.conf.beat_schedule = {}

                    for _socket in _processor.sockets:
                        if _socket.interval <= 0:
                            continue

                        # TODO: QUEUENAME
                        tkey = (
                            _socket.queue.name
                            + "."
                            + fix(_processor.name)
                            + "."
                            + _socket.task.name
                        )

                        worker_queue = KQueue(
                            tkey,
                            Exchange(_socket.queue.name, type="direct"),
                            routing_key=tkey,
                            message_ttl=_socket.queue.message_ttl,
                            durable=_socket.queue.durable,
                            expires=_socket.queue.expires,
                            # TODO: These attributes need to come from Queue model
                            queue_arguments={"x-message-ttl": 30000, "x-expires": 300},
                        )
                        """
                        worker.app.conf.beat_schedule[self.processor.module+'.'+socket.task.name] = {
                            "task": self.processor.module+'.'+socket.task.name,
                            "args": ("Hello World!",),
                            "schedule": socket.interval,
                            'options': {'queue': tkey},
                        }
                        """

                sys.path.insert(0, os.getcwd())

                logging.info("Setting worker")
                setattr(builtins, "worker", worker)

                logging.info("CWD %s", os.getcwd())
                logging.info("PTYHON %s", sys.executable)

                """ Import the module of the processor """
                logging.info("Importing processor module %s", _processor.module)
                try:
                    module = importlib.import_module(_processor.module)
                except:
                    import traceback

                    print(traceback.format_exc())
                    pass

                _plugs = {}

                logging.info("Initializing plugs")
                for plug in _processor.plugs:
                    _plugs[plug.queue.name] = []

                logging.info("Configuring sockets")
                if _processor and _processor.sockets and len(_processor.sockets) > 0:
                    logging.info("Found sockets %s", _processor.sockets)
                    for _socket in _processor.sockets:
                        logging.info(
                            "Configuring socket %s %s", _socket.scheduled, _socket
                        )
                        if _socket.scheduled:
                            logging.info("Socket is scheduled.")
                            try:
                                if _socket.schedule_type == "CRON":
                                    logging.info("ADDING CRON JOB TYPE")

                                elif _socket.schedule_type == "INTERVAL":
                                    logging.info(
                                        "Found INTERVAL schedule for socket: %s",
                                        _socket,
                                    )
                                    if _socket.name not in self.jobs:
                                        logging.info("Adding job-> %s", _socket.name)
                                        plug = None
                                        for plug in _processor.plugs:
                                            if plug.target.name == _socket.name:
                                                break

                                        if plug is None:
                                            logging.error("Job plug is NONE")
                                        else:
                                            # execute sql to get jobs
                                            found = False or _socket.interval <= 0

                                            if not found:
                                                # Ensure job id matches socket so it can be related
                                                # Maybe this shouldn't use a plug
                                                try:
                                                    logging.info(
                                                        "Adding job %s with interval %s",
                                                        dispatcher,
                                                        _socket.interval,
                                                    )

                                                    def schedule_function(
                                                        func, interval, args
                                                    ):
                                                        import sched
                                                        import time

                                                        def call_function(
                                                            scheduler,
                                                            func,
                                                            interval,
                                                            args,
                                                        ):
                                                            logging.info(
                                                                "Calling function %s %s",
                                                                func,
                                                                args,
                                                            )
                                                            func(*args)

                                                            # logging.info(
                                                            #    "Sleeping %s", interval
                                                            # )
                                                            # time.sleep(interval)

                                                            scheduler.enter(
                                                                interval,
                                                                1,
                                                                call_function,
                                                                (
                                                                    scheduler,
                                                                    func,
                                                                    interval,
                                                                    args,
                                                                ),
                                                            )

                                                        s = sched.scheduler(
                                                            time.time, time.sleep
                                                        )
                                                        s.enter(
                                                            interval,
                                                            1,
                                                            call_function,
                                                            (s, func, interval, args),
                                                        )
                                                        s.run()
                                                        logging.info(
                                                            "Scheduler completed."
                                                        )

                                                    logging.info(
                                                        "Pre-dispatch plug.argument %s",
                                                        plug.argument_id,
                                                    )

                                                    job = Thread(
                                                        target=schedule_function,
                                                        args=(
                                                            dispatcher,
                                                            _socket.interval,
                                                            (
                                                                _processor.id,
                                                                plug.id,
                                                                "message",
                                                                _socket.id,
                                                            ),
                                                        ),
                                                    )
                                                    job.start()
                                                    # scheduler.add_job(dispatcher, 'interval', (self.processor, plug, "message", self.dburi, socket), jobstore='default',
                                                    #                    misfire_grace_time=60, coalesce=True, max_instances=1, seconds=socket.interval, id=self.processor.name+plug.name, )
                                                    logging.info(
                                                        "Scheduled socket %s",
                                                        _socket.name,
                                                    )
                                                except:
                                                    import traceback

                                                    logging.info(
                                                        "%s", traceback.format_exc()
                                                    )
                                                    logging.info(
                                                        "Job %s already scheduled.",
                                                        _socket.name,
                                                    )

                            except:
                                import traceback

                                print(traceback.format_exc())
                                logging.info(
                                    "Already scheduled this socket %s", socket.name
                                )

                        logging.info("Printing task...")
                        logging.info("Socket task %s", _socket.task)
                        if _socket.task.code and not _socket.task.endpoint:
                            # We have custom code for this task
                            # Add the task.code to the loaded module
                            # The task.code must have the named function
                            # contained in socket.task.name

                            # Inject the code into the module.
                            # The module originates in the mounted git repo
                            # So the task code is like a "mixin"
                            logging.info("TASK CODE: %s", _socket.task.code)
                            exec(_socket.task.code, module.__dict__)
                        else:
                            logging.info("NO TASK CODE")

                        # Get the function from the loaded module
                        _func = getattr(module, _socket.task.name)

                        logging.info(
                            "TASK SOURCE: %s %s %s",
                            _socket.task.id,
                            _socket.task,
                            _socket.task.source,
                        )

                        # Get the source code of the task function
                        _source = inspect.getsource(_func)

                        session.add(_socket.task)

                        # Add the source code to the task object.
                        # NOTE: This field is different from task.code which
                        # is an override. The task.source is the source from
                        # the configured module function (pulled from git repo)
                        _socket.task.source = _source
                        logging.info(
                            "Updated source for %s %s %s",
                            _socket.task.id,
                            _socket.task,
                            _socket.task.source,
                        )
                        session.commit()
                        logging.info(
                            "TASK SOURCE:-> %s %s %s",
                            _socket.task.id,
                            _socket.task,
                            _socket.task.source,
                        )

                        # TODO: Encase the meta funtion and all the task signals into a loaded class
                        # such that for different processor types, the correct class is loaded

                        def gate_function(*args, **kwargs):
                            pass

                        def wrapped_function(*args, **kwargs):
                            """Main meta function that tracks arguments and dispatches to the user code"""

                            redisclient = redis.Redis.from_url(
                                CONFIG.get("redis", "uri")
                            )

                            logging.info("WRAPPED FUNCTION INVOKE %s", _socket.task)
                            logging.info("ARGS: %s, KWARGS: %s", args, kwargs)

                            taskid = kwargs["myid"]

                            _kwargs = kwargs["kwargs"] if "kwargs" in kwargs else None

                            if "argument" in kwargs:
                                """This means we are invoking on a single argument only"""
                                argument = kwargs["argument"]

                                # Store argument in redis
                                logging.info("ARGS %s %s %s", type(args), args, *args)

                                # We are receiving an argument as a tuple, therefore only the first
                                # element of the tuple is our data
                                _argdata = args[0]
                                _jsonargdata = json.dumps(_argdata)

                                logging.info(
                                    "STORING ARGUMENT  %s %s",
                                    argument["key"]
                                    + "."
                                    + argument["name"]
                                    + "."
                                    + str(argument["position"]),
                                    _jsonargdata,
                                )
                                redisclient.set(
                                    argument["key"]
                                    + "."
                                    + argument["name"]
                                    + "."
                                    + str(argument["position"]),
                                    _jsonargdata,
                                )

                                # args = redisclient.get(argument['key']+'.*')
                                # Compare args names to task arguments and if they are 1 to 1
                                # then trigger the function
                                logging.info("WRAPPED FUNCTION ARGUMENT %s ", argument)

                                # If we received an argument and not all the arguments needed have been stored
                                # then we simply return the argument, otherwise we execute the function
                                _newargs = []
                                for arg in _socket.task.arguments:
                                    if (
                                        arg.kind != Parameter.POSITIONAL_ONLY
                                        and arg.kind != Parameter.POSITIONAL_OR_KEYWORD
                                    ):
                                        continue

                                    _argdata = redisclient.get(
                                        argument["key"]
                                        + "."
                                        + arg.name
                                        + "."
                                        + str(arg.position)
                                    )

                                    if _argdata is None:
                                        logging.info(
                                            "ARGUMENT NOT SATISIFIED %s",
                                            argument["key"]
                                            + "."
                                            + arg.name
                                            + "."
                                            + str(arg.position),
                                        )
                                        return argument
                                    else:
                                        _arg = json.loads(_argdata)
                                        logging.info(
                                            "FOUND STORED ARGUMENT %s %s",
                                            _arg,
                                            argument["key"]
                                            + "."
                                            + arg.name
                                            + "."
                                            + str(arg.position),
                                        )
                                        _newargs.append(_arg)
                                    logging.info("WRAPPED_FUNCTION ARG: %s", arg)

                                args = _newargs

                            source = inspect.getsource(execute_function)

                            # Build the function wrapper call for container execution
                            _call = 'execute_function("{}", "{}", "{}")'.format(
                                taskid, _socket.task.module, _socket.task.name
                            )

                            import pickle

                            # TODO: Load processor decorator class here
                            # TODO: Add sourceplug names to _kwargs

                            """ MAIN FUNCTION EXECUTION """
                            if _kwargs:
                                """If we have kwargs to pass in"""
                                logging.info("Invoking function %s %s", args, _kwargs)

                                logging.info(
                                    "CONTAINER INIT: %s %s",
                                    self.container,
                                    _processor.use_container,
                                )
                                if self.container and _processor.use_container:
                                    # Run function in container and get result
                                    with open("out/" + taskid + ".py", "w") as pfile:
                                        pfile.write(source + "\n")
                                        pfile.write(_call + "\n")

                                    if True:
                                        # Run command inside self.container passing in task id, module and function
                                        pythoncmd = "python /tmp/" + taskid + ".py"
                                        logging.debug("Invoking %s", pythoncmd)

                                        logging.debug("CONTAINER RUN: %s", pythoncmd)

                                        # TODO: Get stdout, stderr and save
                                        # Publish to redis
                                        run = self.container.exec_run(pythoncmd)
                                        output = run.output.decode("utf-8")
                                        redisclient.set(taskid + "-output", output)
                                        outputj = {
                                            "type": "output",
                                            "taskid": taskid,
                                            "output": output,
                                            "processor": _processor.name,
                                        }
                                        redisclient.publish(
                                            "global", json.dumps(outputj)
                                        )
                                        logging.debug("OUT PATH %s", "out/" + taskid)
                                        # Unpickle output and return it
                                    else:
                                        # Run new non-detached container for task
                                        raise NotImplementedError
                                else:
                                    import io
                                    from contextlib import redirect_stdout

                                    # Execute the function inside this celery worker
                                    result = None
                                    # blah blah lots of code ...
                                    with io.StringIO() as buf, redirect_stdout(buf):
                                        # TODO: Load processor class wrapper here
                                        # The processor class will decorate the function and
                                        # instrument the parameters and the response value
                                        # For example, a JSONStore processor might wrap the function
                                        # passing in a metadata object containing the collection to use
                                        # then storing the result in that collection in the JSONStore
                                        # Or it doesn't call the _func at all because there is no user code
                                        # It simple accepts the incoming arguments and stores them
                                        result = _func(*args, **_kwargs)
                                        output = buf.getvalue()
                                        logging.debug("%s OUTPUT: %s", _func, output)
                                        redisclient.set(taskid + "-output", output)
                                        outputj = {
                                            "type": "output",
                                            "taskid": taskid,
                                            "output": output,
                                            "processor": _processor.name,
                                        }
                                        redisclient.publish(
                                            "global", json.dumps(outputj)
                                        )
                                    return result
                                    # return _func(*args, **_kwargs)
                            else:
                                """If we only have args to pass in"""
                                logging.debug("Invoking function %s", args)

                                logging.info(
                                    "CONTAINER INIT: %s %s",
                                    self.container,
                                    _processor.use_container,
                                )
                                if self.container and _processor.use_container:
                                    # Run function in container and get result
                                    with open("out/" + taskid + ".py", "w") as pfile:
                                        pfile.write(source + "\n")
                                        pfile.write(_call + "\n")

                                    if True:
                                        # Run command inside self.container
                                        with open(
                                            "out/" + taskid + ".kwargs", "wb"
                                        ) as kwargsfile:
                                            pickle.dump(kwargs, kwargsfile)
                                        with open(
                                            "out/" + taskid + ".args", "wb"
                                        ) as argsfile:
                                            pickle.dump(args, argsfile)

                                        pythoncmd = "python /tmp/" + taskid + ".py"
                                        logging.debug("Invoking %s", pythoncmd)

                                        logging.debug("CONTAINER RUN: %s", pythoncmd)
                                        res = self.container.exec_run(pythoncmd)
                                        output = res.output.decode("utf-8")
                                        logging.debug("OUTPUT: %s", output)
                                        redisclient.set(taskid + "-output", output)
                                        outputj = {
                                            "type": "output",
                                            "taskid": taskid,
                                            "output": output,
                                            "processor": _processor.name,
                                        }
                                        redisclient.publish(
                                            "global", json.dumps(outputj)
                                        )
                                        result = None
                                        with open(
                                            "out/" + taskid + ".out", "rb"
                                        ) as outfile:
                                            result = pickle.load(outfile)

                                        try:
                                            """Remove state files"""
                                            os.remove("out/" + taskid + ".kwargs")
                                            os.remove("out/" + taskid + ".args")
                                            os.remove("out/" + taskid + ".out")
                                        except Exception as ex:
                                            logging.warning(ex)
                                        finally:
                                            return result

                                    else:
                                        raise NotImplementedError
                                else:
                                    import io
                                    from contextlib import redirect_stdout

                                    try:
                                        # TODO: Get stdout, stderr
                                        result = None
                                        # blah blah lots of code ...
                                        with io.StringIO() as buf, redirect_stdout(buf):
                                            result = _func(*args)
                                            output = buf.getvalue()
                                            logging.debug(
                                                "%s OUTPUT: %s", _func, output
                                            )
                                            redisclient.set(taskid + "-output", output)
                                            outputj = {
                                                "type": "output",
                                                "taskid": taskid,
                                                "output": output,
                                                "processor": _processor.name,
                                            }
                                            redisclient.publish(
                                                "global", json.dumps(outputj)
                                            )
                                        return result
                                    except Exception as ex:
                                        import traceback

                                        _r = traceback.format_tb(ex.__traceback__)
                                        logging.debug("_R EXCEPTION %s", _r)
                                        _ex = TaskInvokeException()
                                        _ex.tb = _r
                                        _ex.exception = ex
                                        raise _ex from ex
                                    finally:
                                        pass
                                        # sys.stdout = old_stdout

                        # If processor is script
                        func = self.celery.task(
                            wrapped_function,
                            name=_processor.module + "." + _socket.task.name,
                            retries=_processor.retries,
                        )
                        logging.debug(
                            "TASK: %s", _processor.module + "." + _socket.task.name
                        )
                        for plug in _socket.targetplugs:
                            func = self.celery.task(
                                wrapped_function,
                                name=plug.queue.name
                                + "."
                                + _processor.module
                                + "."
                                + _socket.task.name,
                                retries=_processor.retries,
                            )
                            logging.debug(
                                "PLUG TASK: %s",
                                plug.queue.name
                                + "."
                                + _processor.module
                                + "."
                                + _socket.task.name,
                            )

                        logging.debug("TASK KEYS: %s", current_app.tasks.keys())
                        """
                        Everything that hosts and runs user code is a processor, but there are different types.
                        Each type handles the meta invocation a bit different.

                        if processor is a gate
                            func = self.celery.task(gate_function, name=self.processor.module +
                            '.' + _socket.task.name, retries=self.processor.retries)

                        if processor is a router
                            func = self.celery.task(router_function, name=self.processor.module +
                            '.' + _socket.task.name, retries=self.processor.retries)
                        """

                        @task_prerun.connect()
                        def pyfi_task_prerun(
                            sender=None, task=None, task_id=None, *args, **kwargs
                        ):
                            """Update args and kwargs before sending to task. Other bookeeping"""
                            from datetime import datetime

                            # PRERUN_CONDITION.acquire()
                            try:
                                logging.debug(
                                    "prerun TASK: %s %s %s", type(task), task, kwargs
                                )

                                if sender.__name__ == "enqueue":
                                    return

                                _function_name = task.name.rsplit(".")[-1:]

                                if "tracking" not in kwargs["kwargs"]:
                                    tracking = str(uuid4())
                                    kwargs["kwargs"]["tracking"] = tracking

                                kwargs["kwargs"]["prerun"] = str(datetime.now())
                                logging.debug(
                                    "KWARGS: %s",
                                    {
                                        "signal": "prerun",
                                        "sender": _function_name[0],
                                        "kwargs": kwargs["kwargs"],
                                        "taskid": task_id,
                                        "tracking": kwargs["kwargs"]["tracking"],
                                        "args": args,
                                    },
                                )
                                run_times[task_id] = time.time()
                                self.main_queue.put(
                                    {
                                        "signal": "prerun",
                                        "sender": _function_name[0],
                                        "kwargs": kwargs["kwargs"],
                                        "tracking": kwargs["kwargs"]["tracking"],
                                        "taskid": task_id,
                                        "args": args,
                                    }
                                )

                                # TODO: Implement throttling here, which is simply a time.sleep(x)
                                # where x is a float that represents period of time. For example
                                # To achieve a throttle of 10/m, x would be 6 seconds
                                # To achieve a throttle of 60/m, x would be 1 second
                                # To achieve a throttle of 1000/m, x would be 0.06 seconds
                                # To achieve a throttle of 1000/h, x would be 0.27 seconds
                                rate_limit = 60 / int(self.data["ratelimit"])
                                logging.debug("Prerun sleeping %s seconds", rate_limit)
                                time.sleep(rate_limit)
                                logging.debug("Done sleeping")

                                logging.debug("Waiting on PRERUN REPLY")
                                response = self.prerun_queue.get()
                                logging.debug("GOT PRERUN QUEUE MESSAGE %s", response)
                                if "error" in response:
                                    logging.error(response["error"])
                                else:
                                    kwargs["kwargs"].update(response)
                                kwargs["kwargs"]["output"] = {}

                                logging.debug("PRERUN QUEUE: %s", response)
                                logging.debug("PRERUN KWARGS IS NOW: %s", kwargs)

                                if "argument" in kwargs["kwargs"]:
                                    _argument = kwargs["kwargs"]["argument"]
                                    key = _argument["key"]
                                # If this is an argument call, then check redis for all current arguments
                                # Including the one here, pull in all the arguments and put them in the kwargs
                                # The wrapped_function will receive them and based on the function arguments
                                # decide if it can invoke the function or not

                            finally:
                                # PRERUN_CONDITION.release()
                                pass

                        @task_success.connect()
                        def pyfi_task_success(sender=None, **kwargs):
                            logging.debug("Task SUCCESS: %s", sender)
                            # Store task run data
                            pass

                        @task_failure.connect()
                        def pyfi_task_failure(sender=None, **kwargs):
                            # Store task run data
                            logging.debug("Task FAILURE: %s %s", sender, kwargs)

                        @task_internal_error.connect()
                        def pyfi_task_internal_error(sender=None, **kwargs):
                            # Store task run data
                            pass

                        @task_received.connect()
                        def pyfi_task_received(sender=None, request=None, **kwargs):
                            try:
                                logging.debug(
                                    "Task RECEIVED REQUEST %s %s %s",
                                    request.id,
                                    sender,
                                    request.name,
                                )

                                _function_name = request.name.rsplit(".")[-1:]
                                logging.debug(
                                    "Task Request Parent %s", request.parent_id
                                )
                                from datetime import datetime

                                sender = request.task_name.rsplit(".")[-1]
                                logging.debug("RECEIVED SENDER: %s", sender)

                                if sender == "enqueue":
                                    return

                                tracking = str(uuid4())
                                logging.debug("KWARGS %s", kwargs)
                                logging.debug(
                                    "RECEIVED KWARGS:",
                                    {
                                        "signal": "received",
                                        "sender": _function_name[0],
                                        "kwargs": {"tracking": tracking},
                                        "request": request.id,
                                        "taskparent": request.parent_id,
                                        "taskid": request.id,
                                    },
                                )
                                message = {
                                    "signal": "received",
                                    "sender": _function_name[0],
                                    "kwargs": {"tracking": tracking},
                                    "request": request.id,
                                    "taskparent": request.parent_id,
                                    "taskid": request.id,
                                }
                                logging.debug(
                                    "pyfi_task_received: main_queue: Put %s", message
                                )
                                self.main_queue.put(message)
                                logging.debug("PUT RECEIVED KWARGS on queue")

                                # Wait for reply
                                logging.debug("WAITING ON received_queue")
                                _kwargs = self.received_queue.get()
                                kwargs.update(_kwargs)
                                logging.debug("GOT RECEIVED REPLY %s", _kwargs)
                                logging.debug("New KWARGS ARE: %s", kwargs)
                            except:
                                print(traceback.format_exc())

                        @task_postrun.connect()
                        def pyfi_task_postrun(
                            sender=None,
                            task_id=None,
                            task=None,
                            retval=None,
                            *args,
                            **kwargs,
                        ):
                            import datetime
                            import traceback

                            if sender.__name__ == "enqueue":
                                return

                            _type = str(type(retval).__name__)

                            _function_name = task.name.rsplit(".")[-1:][0]
                            logging.debug("TASK POSTRUN ARGS: %s", args)
                            logging.debug("TASK POSTRUN RETVAL: %s", retval)

                            logging.debug(
                                "TASK_POSTRUN KWARGS: %s",
                                {
                                    "signal": "postrun",
                                    "result": retval,
                                    "sender": _function_name,
                                    "type": _type,
                                    "kwargs": kwargs["kwargs"],
                                    "taskid": task_id,
                                    "args": args,
                                },
                            )

                            start_time = run_times[task_id]
                            del run_times[task_id]
                            duration = datetime.timedelta(
                                seconds=time.time() - start_time
                            )
                            postrun = {
                                "signal": "postrun",
                                "duration": str(duration),
                                "result": retval,
                                "sender": _function_name,
                                "type": _type,
                                "kwargs": kwargs["kwargs"],
                                "taskid": task_id,
                                "args": args,
                            }

                            logging.debug("POSTRUN PUTTING ON main_queue %s", postrun)
                            self.main_queue.put(postrun)
                            logging.debug("POSTRUN DONE PUTTING ON main_queue")

                logging.info("Starting scheduler...")
                scheduler.start()
                logging.info("Starting worker...")
                worker.start()

        def start_worker_proc():
            # Create or update venv
            from virtualenvapi.manage import VirtualEnvironment

            with get_session() as session:
                deployment = (
                    session.query(DeploymentModel)
                    .filter_by(name=self.deploymentname)
                    .first()
                )
                worker = deployment.worker

                logging.debug(
                    "Preparing worker %s %s %s %s %s",
                    worker.name,
                    deployment.processor.name,
                    self.backend,
                    self.broker,
                    deployment.processor.module,
                )

                """ Install gitrepo and build virtualenv """
                if deployment.processor.commit and self.skipvenv:
                    if deployment.processor.commit:
                        os.system("git checkout {}".format(deployment.processor.commit))

                if deployment.processor.gitrepo and not self.skipvenv:

                    if not os.path.exists(self.workpath):
                        logging.debug("MAKING PATH %s", self.workpath)
                        os.makedirs(self.workpath)
                    else:
                        logging.debug("WORKPATH %s exists", self.workpath)

                    os.chdir(self.workpath)

                    if self.usecontainer:
                        """Launch pyfi:latest container passing in variables and gitrepo. Maintain reference to
                        launched container"""
                        raise NotImplementedError
                    else:
                        """Build our virtualenv and import the gitrepo for the processor"""
                        logging.debug(
                            "git clone for processor %s", deployment.processor.name
                        )

                        logging.debug(
                            "git clone -b {} --single-branch {} git".format(
                                deployment.processor.branch,
                                deployment.processor.gitrepo,
                            )
                        )

                        pull = False
                        changes = True

                        logging.debug("Current directory: %s", os.getcwd())

                        if (
                            worker
                            and worker.workerdir
                            and os.path.exists(worker.workerdir)
                            and os.path.exists(worker.workerdir + "/git")
                        ):
                            logging.debug(
                                "Changing to existing work directory %s",
                                worker.workerdir,
                            )
                            os.chdir(worker.workerdir + "/git")
                            os.system("git config --get remote.origin.url")
                            os.system("git config pull.rebase false")
                            logging.debug("Pulling update from git")
                            output = os.popen("git pull").read()
                            changes = not output == "Already up to date.\n"
                        else:
                            """Clone gitrepo. Retry after 3 seconds if failure"""
                            logging.debug("cwd is %s", os.getcwd())
                            logging.debug("workdir is %s", self.workpath)

                            logging.debug(
                                "Changing to %s for processor %s",
                                self.workpath,
                                deployment.processor.name,
                            )
                            os.chdir(self.workpath)

                            if os.path.exists("git"):
                                os.chdir("git")
                                pull = True
                            else:
                                logging.debug("No existing git directory....")

                            try:
                                if not pull:
                                    logging.debug(
                                        "git clone -b {} --single-branch {} git".format(
                                            deployment.processor.branch,
                                            deployment.processor.gitrepo.split("#")[0],
                                        )
                                    )
                                    os.system(
                                        "git clone -b {} --single-branch {} git".format(
                                            deployment.processor.branch,
                                            deployment.processor.gitrepo.split("#")[0],
                                        )
                                    )
                                    sys.path.append(self.workpath + "/git")
                                    os.chdir("git")
                                else:
                                    sys.path.append(self.workpath + "/git")
                                    output = os.popen("git pull").read()
                                    changes = not output == "Already up to date.\n"

                                os.system("git config credential.helper store")
                                logging.debug("Exited git setup")
                            except Exception as ex:
                                logging.error(ex)

                        if (
                            deployment.processor.commit
                            and not deployment.processor.gittag
                        ):
                            os.system(
                                "git checkout {}".format(deployment.processor.commit)
                            )

                        if deployment.processor.gittag:
                            os.system(
                                "git checkout {}".format(deployment.processor.gittag)
                            )

                        # If not using a container, then build the virtualenv
                        if changes or not os.path.exists("venv/bin/flow"):
                            logging.info(
                                "Building virtualenv for %s...in %s",
                                deployment.processor.name,
                                os.getcwd(),
                            )
                            env = VirtualEnvironment(
                                "venv", python=sys.executable, system_site_packages=True
                            )  # inside git directory

                            login = os.environ["GIT_LOGIN"]
                            branch = "development"

                            if "PYFI_BRANCH" in os.environ:
                                branch = os.environ["PYFI_BRANCH"]

                            pyfi_repo = (
                                "-e git+"
                                + login
                                + "/radiantone/pyfi-private@"
                                + branch
                                + "#egg=pyfi"
                            )
                            logging.info("PYFI_REPO %s", pyfi_repo)
                            # Install pyfi
                            # TODO: Make this URL a setting so it can be overridden
                            env.install("psycopg2")
                            env.install("pymongo")

                            try:
                                env.install(pyfi_repo)
                            except:
                                import traceback

                                print(traceback.format_exc())
                                pass

                            logging.debug(
                                "Deployment use_container %s",
                                deployment.processor.use_container,
                            )
                            if not deployment.processor.use_container:
                                """If we are not running the processor tasks in a container, then load it into the venv"""
                                try:
                                    logging.debug(
                                        "Installing package %s with %s into %s",
                                        deployment.processor.gitrepo.strip(),
                                        sys.executable,
                                        os.getcwd(),
                                    )
                                    env.install(
                                        "-e git+" + deployment.processor.gitrepo.strip()
                                    )
                                    logging.info(
                                        "Installed: -e git+%s"
                                        + deployment.processor.gitrepo.strip()
                                    )
                                    logging.debug(
                                        "Successfully installed %s",
                                        deployment.processor.gitrepo.strip(),
                                    )
                                except:
                                    import traceback

                                    print(traceback.format_exc())
                                    logging.error(
                                        "Could not install %s",
                                        deployment.processor.gitrepo.strip(),
                                    )
                        else:
                            logging.debug(
                                "No rebuild needed. venv already exists in %s",
                                os.getcwd(),
                            )

                # Sometimes we just want to recreate the setup
                if not start:
                    logging.debug("Returning")
                    return

                logging.info("Creating worker process")
                """ Start worker process"""
                worker_process = Process(
                    target=worker_proc,
                    name="worker_proc",
                    args=(self.celery, self.queue, self.dburi),
                )

                logging.debug(
                    "Starting worker_process for %s...%s",
                    self.data["name"],
                    self.worker_process,
                )

                logging.debug("Starting worker process")
                worker_process.start()
                logging.debug(
                    "worker_process started for %s...%s",
                    self.data["name"],
                    self.worker_process,
                )

                with open(self.workpath + "/worker.pid", "w") as pidfile:
                    pidfile.write(str(worker_process.pid))
                    logging.debug(
                        "WROTE PID %s to FILE %s",
                        str(worker_process.pid),
                        self.workpath + "/worker.pid",
                    )

                worker_process.app = self.celery
                # worker_process.daemon = True

                self.process = worker_process
                self.worker_process = worker_process

        """ Send messages to redis pub/sub for consumers """

        ####################################################
        def emit_messages():
            """Get messages off queue and emit to pubsub server"""
            redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))
            from setproctitle import setproctitle

            setproctitle("pyfi worker::emit_messages")
            while True:

                try:
                    message = self.queue.get()
                    logging.debug("Emitting message %s %s", message[1]["room"], message)
                    redisclient.publish(
                        message[1]["room"] + "." + message[1]["channel"],
                        json.dumps(message[1]),
                    )
                    redisclient.publish(
                        "global",
                        json.dumps(message[1]),
                    )
                    # TODO: Also emit to various other channels like "processors","global", etc

                except Exception as ex:
                    logging.error(ex)
                    time.sleep(3)

        def start_emit_messages():
            emit_process = self.emit_process = Thread(
                target=emit_messages, name="emit_messages"
            )
            emit_process.daemon = True
            emit_process.start()
            logging.debug("emit_messages started...")

        """ Health check web server """

        ###############################
        def web_server():
            import bjoern
            from setproctitle import setproctitle

            try:
                setproctitle("pyfi worker::web_server")
                logging.info("Starting worker web server on %s", self.port)

                bjoern.run(app, "0.0.0.0", self.port)
            except Exception as ex:
                logging.error(ex)
                logging.debug("worker web_server: exiting...")

        def start_web_server():
            webserver = Thread(target=web_server)
            webserver.start()
            logging.debug("web_server started...")

        ops = [
            start_database_actions,
            start_worker_proc,
            start_emit_messages,
            start_web_server,
        ]

        # Start all the operations
        [op() for op in ops]

        logging.debug("Returning worker_process %s", self.process)

        return self.process

    def busy(self):
        """
        Docstring
        """
        # cinspect = celery.current_app.control.inspect()
        # cinspect.active()) + ccount(cinspect.scheduled()) + ccount(cinspect.reserved())
        pass

    def suspend(self):
        """
        Docstring
        """
        p = psutil.Process(self.process.pid)
        p.suspend()
        self.scheduler.pause()

    def resume(self):
        """
        Docstring
        """
        p = psutil.Process(self.process.pid)
        p.resume()
        self.scheduler.resume()

    #########################################################################
    # Kill worker thread
    #########################################################################
    def kill(self):
        """
        Docstring
        """
        logging.debug("Terminating worker %s", self.workpath)

        with open(self.workpath + "/git/worker.pid") as pidfile:
            pid = int(pidfile.read())

            process = psutil.Process(pid)

            # logging.debug("Killing worker PID %s for %s",self.process.pid, self.data['name'])

            logging.debug("Killing worker_proc thread for %s", self.data["name"])
            # self.worker_process.raise_exception()
            # self.worker_process.join()
            logging.debug("Killed worker_proc thread for %s", self.data["name"])

            for child in process.children(recursive=True):
                try:
                    child.kill()
                except:
                    pass

            # process.kill()
            process.terminate()

            # os.killpg(pid, 15)
            # os.kill(pid, signal.SIGKILL)

            logging.debug("Finishing %s", self.workpath)

            try:
                logging.debug("Waiting for process to finish")
                self.process.join()
                logging.debug("Process finished")
            except:
                pass

            if os.path.exists(self.workpath) and not KEEP_WORKER_DIRS:
                logging.debug("Removing working directory %s", self.workpath)
                shutil.rmtree(self.workpath)

            logging.debug("Done killing worker %s", self.workpath)


@app.route("/kill")
def kill():
    from flask import request

    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@app.route("/")
def hello():
    import json

    return json.dumps({"status": "green"})
