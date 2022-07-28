"""
Agent workerclass. Primary task/code execution context for processors. This is where all the magic happens
"""
import configparser
import gc
import inspect
import logging

# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
import os
import platform
import shutil
import signal
import sys
import tracemalloc

import psutil
import redis

tracemalloc.start()
from functools import partial
from inspect import Parameter
from multiprocessing import Condition, Queue
from pathlib import Path

from flask import Flask
from pytz import utc

app = Flask(__name__)

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from kombu import Exchange
from kombu import Queue as KQueue
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool

from celery import Celery
from celery import chain as pipeline
from celery import group as parallel
from celery.signals import (
    after_task_publish,
    setup_logging,
    task_failure,
    task_internal_error,
    task_postrun,
    task_prerun,
    task_received,
    task_success,
    worker_process_init,
)
from pyfi.db.model import (
    ActionModel,
    AgentModel,
    CallModel,
    EventModel,
    FlowModel,
    JobModel,
    LogModel,
    NodeModel,
    PlugModel,
    ProcessorModel,
    QueueModel,
    RoleModel,
    SettingsModel,
    SocketModel,
    TaskModel,
    UserModel,
    WorkerModel,
)
from pyfi.db.model.models import DeploymentModel, use_identity

PRERUN_CONDITION = Condition()
POSTRUN_CONDITION = Condition()


@setup_logging.connect
def setup_celery_logging(**kwargs):
    logging.debug("DISABLE LOGGING SETUP")


# Set global vars
HOME = str(Path.home())
CONFIG = configparser.ConfigParser()

# Load the config
if os.path.exists(HOME + "/pyfi.ini"):
    CONFIG.read(HOME + "/pyfi.ini")

DBURI = CONFIG.get("database", "uri")

# Create database engine
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

logging.info("OS PID is {}".format(os.getpid()))


def fix(name):

    return name.replace(" ", ".")


def execute_function(taskid, mname, fname, *args, **kwargs):
    """Executor for container based tasks"""
    import importlib
    import pickle
    from uuid import uuid4

    print("Execute function", taskid, mname, fname)

    _args = args
    _kwargs = kwargs

    with open("/tmp/" + taskid + ".args", "rb") as argsfile:
        _args = pickle.load(argsfile)

    with open("/tmp/" + taskid + ".kwargs", "rb") as kwargsfile:
        _kwargs = pickle.load(kwargsfile)

    _module = importlib.import_module(mname)
    _function = getattr(_module, fname)

    result = _function(*_args, **_kwargs)

    print("RESULT: ", result)
    with open("/tmp/" + taskid + ".out", "wb") as rfile:
        pickle.dump(result, rfile)
        print("DUMPED OUT:", "/tmp/" + taskid + ".out")

    return result


def shutdown(*args):
    """Shutdown worker"""
    from psutil import Process

    logging.info("Shutting down...")
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


def dispatcher(processor, plug, message, session, socket, **kwargs):
    """Execute a task based on a schedule"""
    logging.info("Dispatching %s PLUG %s", socket, plug)
    backend = CONFIG.get("backend", "uri")
    broker = CONFIG.get("broker", "uri")
    celery = Celery(backend=backend, broker=broker, include=processor.module)
    logging.info("TASK NAMES: %s", celery.tasks.keys())
    try:
        name = plug.name

        if plug is None:
            logging.warning("Plug %s does not exist", name)
            return

        logging.debug("PLUG RESULT %s", plug is not None)

        # TODO: QUEUENAME
        tkey = socket.queue.name + "." + fix(processor.name) + "." + socket.task.name
        # tkey = socket.queue.name
        logging.info("DISPATCH TKEY %s", tkey)
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

        logging.info("Plug.argument %s", plug.argument)
        if plug.argument:
            logging.info(
                "Processor plug %s is connected to argument: %s", plug, plug.argument
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

            logging.info("Plug argument %s", plug.argument)
            kwargs["argument"] = argument
        else:
            logging.info("Processor plug %s is not connected to argument.", plug)

        kwargs["function"] = socket.task.name

        task_sig = celery.signature(
            processor.module + "." + socket.task.name, queue=queue, kwargs=kwargs
        )

        delayed = task_sig.delay(message)

        logging.info("Dispatched %s", delayed)
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

    from contextlib import contextmanager

    container = None
    _session = None
    _connection = None

    @contextmanager
    def get_session(self, engine):
        """Creates a context with an open SQLAlchemy session."""
        logging.info("Connecting DB")

        if not self._session:
            logging.info("Creating scoped session")
            self._session = scoped_session(self.sm)
            # self._session = scoped_session(
            #    sessionmaker(autocommit=False, autoflush=True, bind=engine)
            # )
        logging.info("Yielding session")
        yield self._session
        self._session.commit()
        self._session.flush()
        """
        logging.info("Closing session")
        db_session.close()
        logging.info("Closing connection")
        connection.close()
        """

    def __init__(
        self,
        processor: ProcessorModel,
        workdir: str,
        pool: int = 4,
        port: int = 8020,
        size: int = 10,
        deployment: DeploymentModel = DeploymentModel,
        database=None,
        user: UserModel = UserModel,
        usecontainer: bool = False,
        workerport: int = 8020,
        skipvenv: bool = False,
        backend: str = "redis://localhost",
        hostname: str = None,
        agent: AgentModel = AgentModel,
        celeryconfig=None,
        broker: str = "pyamqp://localhost",
    ):
        """ """
        import multiprocessing

        from pyfi.db.model import Base

        global HOSTNAME

        self.processor = processor

        self.worker = deployment.worker
        self.deployment = deployment
        self.backend = backend
        self.broker = broker
        self.port = port
        self.workdir = workdir
        self.dburi = database
        self.skipvenv = skipvenv
        self.usecontainer = usecontainer
        self.size = size
        self.agent = agent
        self.port = workerport

        if hostname:
            HOSTNAME = hostname
            self.hostname = hostname
            logging.info("HOSTNAME is {}".format(hostname))
        else:
            hostname = HOSTNAME

        # Publish queue
        self.queue = Queue()

        # Main message database queue
        self.main_queue = Queue(self.size)

        # Received events
        self.received_queue = Queue()

        # Prerun events
        self.prerun_queue = Queue()

        # Postrun events
        self.postrun_queue = Queue()

        cpus = multiprocessing.cpu_count()
        self.database = DATABASE

        sm = sessionmaker(bind=self.database)
        self.sm = sm

        self.pool = pool
        self.user = user
        self.pwd = os.getcwd()

        logging.debug("New Worker init: %s", processor)

        if os.path.exists(HOME + "/pyfi.ini"):
            CONFIG.read(HOME + "/pyfi.ini")
            self.backend = CONFIG.get("backend", "uri")
            self.broker = CONFIG.get("broker", "uri")

            """
            jobstores = {
                'default': SQLAlchemyJobStore(url=CONFIG.get('database', 'uri'), metadata=Base.metadata, tablename=processor.name+'_jobs')
            }
            """
            executors = {
                "default": ThreadPoolExecutor(20),
                "processpool": ProcessPoolExecutor(5),
            }
            job_defaults = {"coalesce": False, "max_instances": 3}

            self.scheduler = BackgroundScheduler(
                job_defaults=job_defaults, timezone=utc
            )

            self.jobs = {}

            logging.debug("JOBS %s", self.jobs)

            self.scheduler.print_jobs()

        if celeryconfig is not None:
            logging.info("Applying celeryconfig from %s", celeryconfig)
            import importlib

            module = importlib.import_module(celeryconfig.split["."][:-1])
            celeryconfig = getattr(module, celeryconfig.split["."][-1:])
            self.celery = Celery(include=self.processor.module)
            self.celery.config_from_object(celeryconfig)

        else:
            self.celery = Celery("pyfi", backend=backend, broker=broker)

            from pyfi.celery import config

            logging.info("App config is %s", config)
            self.celery.config_from_object(config)

        @self.celery.task(name=self.processor.name + ".pyfi.celery.tasks.enqueue")
        def enqueue(data, *args, **kwargs):
            logging.info("ENQUEUE: %s", data)
            return data

        with self.get_session(self.database) as session:
            logging.info("Retrieving deployment by name %s", deployment.name)
            _deployment = (
                session.query(DeploymentModel).filter_by(name=deployment.name).first()
            )
            _processor = (
                session.query(ProcessorModel).filter_by(name=processor.name).first()
            )

            workerModel = self.workerModel = (
                session.query(WorkerModel)
                .filter_by(name=hostname + ".agent." + self.processor.name + ".worker")
                .first()
            )
            workers = session.query(WorkerModel).filter_by(hostname=hostname).all()

            logging.info("Found worker {}".format(workerModel))

            workerModel = None

            for worker in workers:
                if worker.deployment and worker.deployment.name == _deployment.name:
                    workerModel = worker
                    break

            if workerModel is not None:
                logging.info("Worker deployment is {}".format(workerModel.deployment))
                logging.info("Found %s workers for %s", len(workers), hostname)

            if workerModel is None:
                logging.info("Creating new worker for %s", _deployment)
                workerModel = self.workerModel = WorkerModel(
                    name=HOSTNAME
                    + ".agent."
                    + self.processor.name
                    + ".worker."
                    + str(len(workers) + 1),
                    concurrency=int(_deployment.cpus),
                    status="ready",
                    backend=self.backend,
                    broker=self.broker,
                    processor=_processor,
                    agent_id=self.agent.id,
                    deployment=_deployment,
                    workerdir=self.workdir,
                    hostname=HOSTNAME,
                    requested_status="start",
                )

                logging.info("Created workerModel")
                # session.merge(deployment)
                if not workerModel.agent_id:
                    workerModel.agent_id = self.agent.id

                session.add(workerModel)
                logging.info("Added workerModel to session %s", workerModel)
                session.commit()

            workerModel.workerdir = self.workdir
            workerModel.port = self.port

            # logging.info("Adding deployment %s to worker model", _deployment)
            workerModel.deployment = _deployment
            _deployment.worker = workerModel
            _deployment.worker.processor = _processor
            logging.info("Refreshing processor")
            # session.refresh(_processor)
            # logging.info("Printing processor")
            # logging.info("Attached worker to deployment and processor...%s",_processor)
            # session.commit()
            logging.info("Attached worker: Done")

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
        from multiprocessing import Process
        from subprocess import Popen

        """
        This method is used by the agent after the Worker() has been created and configured its venv.
        It is then launched using a subprocess running from that virtualenv
        The 'pyfi worker start' command will itself, run the start() method below.

        workerproc = Popen(["venv/bin/pyfi","worker","start","-n",processor['processor'].worker.name])
        """

        if not self.usecontainer:
            cmd = [
                "venv/bin/flow",
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
                    "venv/bin/flow",
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

            logging.info("Launching worker %s %s", cmd, name)
            self.process = process = Popen(
                cmd, stdout=sys.stdout, stderr=sys.stdout, preexec_fn=os.setsid
            )

            with open(self.pwd + "/worker.pid", "a") as pidfile:
                pidfile.write(str(process.pid))

            logging.debug("Worker launched successfully: process %s.", self.process.pid)
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
        import threading
        import time
        from multiprocessing import Process

        import bjoern

        def do_work():
            # Retrieve workmodels where worker=me and execute them
            pass

        def database_actions():
            """Main database interaction thread. Receives signals off a queue
            and conducts database operations based on the message"""
            from datetime import datetime
            from uuid import uuid4

            while True:
                with self.get_session(self.database) as session:
                    processor = (
                        session.query(ProcessorModel)
                        .filter_by(id=self.processor.id)
                        .first()
                    )
                    # snapshot=tracemalloc.take_snapshot()
                    # for i, stat in enumerate(snapshot.statistics('filename')[:5], 1):
                    #    logging.info("top_current %s %s", i, stat)

                    # session.refresh(processor)
                    # Check if any work has been assigned to me and then do it
                    # This will pause the task execution for this worker until the
                    # work is complete
                    do_work()

                    _plugs = {}

                    logging.info("DBACTION: Processor %s", processor)
                    logging.info(
                        "Checking main_queue[%s] with %s items",
                        self.size,
                        self.main_queue.qsize(),
                    )
                    logging.info("---")
                    logging.info("---")
                    _signal = self.main_queue.get()
                    logging.info("---")
                    logging.info("---")
                    logging.info("SIGNAL: %s", _signal)

                    if _signal["signal"] == "received":
                        logging.info("RECEIVED SIGNAL %s", _signal)

                        for _socket in processor.sockets:
                            if _socket.task.name == _signal["sender"]:
                                logging.info(
                                    "RECEIVED SIGNAL: FOUND TASK %s", _socket.task
                                )
                                parent = None

                                received = datetime.now()
                                logging.info("Found socket: %s", _socket)

                                if "parent" not in _signal["kwargs"]:
                                    _signal["kwargs"]["parent"] = str(uuid4())
                                    logging.info(
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
                                    resultid="celery-task-meta-" + _signal["taskid"],
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
                                logging.info(
                                    "CREATED CALL %s %s", myid, _signal["taskid"]
                                )

                                self.queue.put(_data)
                                self.received_queue.put(_signal["kwargs"])

                    if _signal["signal"] == "prerun":
                        logging.info("Task PRERUN: %s", _signal)

                        for _socket in processor.sockets:
                            if _socket.task.name == _signal["sender"]:

                                parent = None

                                started = datetime.now()
                                if "parent" not in _signal["kwargs"]:
                                    _signal["kwargs"]["parent"] = str(uuid4())
                                    logging.info(
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
                                logging.info(
                                    "SOCKET TARGET PLUGS %s", _socket.sourceplugs
                                )

                                # TODO: Still needed?
                                for source in _socket.sourceplugs:
                                    logging.info(
                                        "SOCKET QUEUE IS %s, SOURCE QUEUE is %s",
                                        _socket.queue.name,
                                        source.queue.name,
                                    )
                                    if source.queue.name == _socket.queue.name:
                                        sourceplug = source
                                        break

                                logging.info("Looking up call %s", _signal["taskid"])
                                call = (
                                    session.query(CallModel)
                                    .filter_by(celeryid=_signal["taskid"])
                                    .first()
                                )

                                if call is None:
                                    logging.info("Sleeping 1...")
                                    time.sleep(1)

                                    logging.info(
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

                                    logging.info("RETRIEVED CALL %s", call)

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
                                logging.info(
                                    "Putting %s on PRERUN_QUEUE", _signal["kwargs"]
                                )
                                self.prerun_queue.put(_signal["kwargs"])
                                logging.info(
                                    "Done Putting %s on PRERUN_QUEUE", _signal["kwargs"]
                                )

                    if _signal["signal"] == "postrun":
                        """
                        Task has completed, now we need to determine how to send the results to downstream plugs
                        """
                        import json
                        import pickle
                        from datetime import datetime

                        logging.info("POSTRUN: SIGNAL: %s", _signal)
                        logging.info("POSTRUN: KWARGS: %s", _signal["kwargs"])
                        task_kwargs = _signal["kwargs"]
                        plugs = task_kwargs["plugs"]

                        pass_kwargs = {}

                        if "tracking" in task_kwargs:
                            pass_kwargs["tracking"] = task_kwargs["tracking"]
                        if "parent" in task_kwargs:
                            pass_kwargs["parent"] = task_kwargs["parent"]
                            logging.info("SETTING PARENT: %s", pass_kwargs)

                        myid = task_kwargs["myid"]
                        pass_kwargs["postrun"] = str(datetime.now())

                        try:
                            # Is there a call already associated with this task? There should be!
                            call = session.query(CallModel).filter_by(id=myid).first()

                            logging.info("CALL QUERY %s", call)

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

                                session.add(event)
                                call.events += [event]
                                session.add(call)
                                session.commit()
                            else:
                                logging.warning(
                                    "No pre-existing Call object for id %s", myid
                                )
                        except:
                            logging.error("No pre-existing Call object for id %s", myid)

                        sourceplugs = {}
                        data = {
                            "module": self.processor.module,
                            "date": str(datetime.now()),
                            "resultkey": "celery-task-meta-" + _signal["taskid"],
                            "message": "Processor message",
                            "channel": "task",
                            "room": processor.name,
                            "task": _signal["sender"],
                        }

                        # Dispatch result to connected plugs
                        for socket in processor.sockets:

                            # Find the socket associated with this task
                            if socket.task.name == _signal["sender"]:

                                for plug in socket.sourceplugs:
                                    _plugs[plug.name] = []
                                    sourceplugs[plug.name] = plug

                                # Build path to the task
                                processor_path = (
                                    socket.queue.name
                                    + "."
                                    + processor.name.replace(" ", ".")
                                )

                                # Create data record for this event
                                data = {
                                    "module": self.processor.module,
                                    "date": str(datetime.now()),
                                    "resultkey": "celery-task-meta-"
                                    + _signal["taskid"],
                                    "message": "Processor message",
                                    "channel": "task",
                                    "room": processor.name,
                                    "task": _signal["sender"],
                                }

                                payload = json.dumps(data)
                                data["message"] = payload
                                break

                        # Add task result to data record
                        _r = _signal["result"]
                        logging.info("RESULT2: %s %s", type(_r), _r)
                        try:
                            result = json.dumps(_r, indent=4)
                        except:
                            result = str(_r)

                        data["duration"] = _signal["duration"]
                        data["message"] = json.dumps(result)
                        data["message"] = json.dumps(data)
                        data["error"] = False
                        from urllib.parse import urlparse

                        from rejson import Client, Path

                        logging.info("REDIS JSON: Connecting to %s", self.backend)
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
                        logging.info(
                            "REDIS JSON:%s %s",
                            "celery-task-result-" + _signal["taskid"],
                            _r,
                        )

                        if isinstance(_r, TaskInvokeException):
                            data["error"] = True
                            data["message"] = _r.tb

                        data["state"] = "postrun"

                        logging.info("DATA2: %s", data)
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

                        logging.info("PLUGS-: %s", plugs)

                        pipelines = []

                        for pname in sourceplugs:
                            logging.info("PLUG Pname: %s", pname)
                            processor_plug = None

                            if pname not in sourceplugs:
                                logging.warning("%s plug not in %s", pname, sourceplugs)
                                continue

                            processor_plug = sourceplugs[pname]

                            if data["error"] and processor_plug.type != "ERROR":
                                logging.info(
                                    "Skipping non-error processor plug {} for data error {}".format(
                                        processor_plug, data
                                    )
                                )
                                continue

                            logging.info("Using PLUG: %s", processor_plug)

                            if processor_plug is None:
                                logging.warning(
                                    "No plug named [%s] found for processor[%s]",
                                    pname,
                                    processor.name,
                                )
                                continue

                            target_processor = (
                                session.query(ProcessorModel)
                                .filter_by(id=processor_plug.target.processor_id)
                                .first()
                            )

                            key = processor_plug.target.queue.name

                            msgs = [(result, _r)]

                            logging.info("msgs %s", msgs)

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

                                # TODO: QUEUENAME Should this just be key?
                                tkey = (
                                    key
                                    + "."
                                    + fix(target_processor.name)
                                    + "."
                                    + processor_plug.target.task.name
                                )

                                tkey2 = key + "." + processor_plug.target.task.name

                                logging.info("Sending {} to queue {}".format(msg, tkey))

                                if processor_plug.target.queue.qtype == "direct":
                                    logging.info("Finding processor....")

                                    socket = processor_plug.target

                                    logging.info(
                                        "Invoking {}=>{}({})".format(
                                            key,
                                            target_processor.module
                                            + "."
                                            + processor_plug.target.task.name,
                                            msg,
                                        )
                                    )

                                    """
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
                                    # TODO: Task queue
                                    plug_sig = self.celery.signature(
                                        processor.name + ".pyfi.celery.tasks.enqueue",
                                        args=(msg,),
                                        queue=plug_queue,
                                        kwargs=pass_kwargs,
                                    )
                                    """

                                    plug_queue = KQueue(
                                        processor_plug.queue.name,
                                        Exchange(key, type="direct"),
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

                                    logging.info("worker queue %s", worker_queue)
                                    logging.info("task queue %s", worker_queue)
                                    task_sig = None

                                    # Create task signature
                                    try:
                                        logging.info("PASS_KWARGS: %s", pass_kwargs)

                                        if processor_plug.argument:
                                            logging.info(
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
                                            logging.info(
                                                "Processor plug not connected to argument."
                                            )

                                        # PLUG ROUTING
                                        task_sig = self.celery.signature(
                                            processor_plug.queue.name
                                            + "." 
                                            + target_processor.module
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
                                        '''
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
                                        '''
                                        delayed = pipeline(task_sig)
                                        pipelines += [delayed]
                                        logging.info("   ADDED TASK SIG: %s", task_sig)
                                    except:
                                        import traceback

                                        print(traceback.format_exc())

                                    if task_sig:
                                        logging.info(
                                            "call complete %s %s %s %s",
                                            target_processor.module
                                            + "."
                                            + processor_plug.target.task.name,
                                            (msg,),
                                            worker_queue,
                                            task_sig,
                                        )

                        delayed = parallel(*pipelines).delay()

        # Start database session thread. Provides a single thread and active session
        # to perform all database interactions. Receives messages from queue
        dbactions = threading.Thread(target=database_actions)
        dbactions.start()

        def worker_proc(app, _queue, dburi):
            """Main celery worker thread. Configure worker, queues and launch celery worker"""
            import builtins
            import importlib
            import json
            import sys
            import time
            from uuid import uuid4

            from billiard.pool import Pool
            from docker.types import Mount
            from setproctitle import setproctitle

            import docker

            setproctitle("pyfi worker::worker_proc")

            job_defaults = {"coalesce": False, "max_instances": 3}

            scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=utc)

            queues = []
            engine = create_engine(
                dburi,
                pool_size=1,
                max_overflow=5,
                pool_recycle=3600,
                poolclass=QueuePool,
            )

            logging.info("use_container %s", self.processor.use_container)
            if self.processor.use_container:
                agent_cwd = os.environ["AGENT_CWD"]

                client = docker.from_env()
                logging.info(
                    "Worker: Checking processor.detached....%s", self.processor.detached
                )
                if self.processor.detached:
                    logging.info(
                        "Running container %s:%s....",
                        self.processor.container_image,
                        self.processor.container_version,
                    )

                    if not os.path.exists("out"):
                        os.mkdir("out")
                    try:
                        self.container = client.containers.get(
                            HOSTNAME + "." + self.processor.module
                        )
                    except Exception:
                        self.container = client.containers.run(
                            self.processor.container_image
                            + ":"
                            + self.processor.container_version,
                            auto_remove=True,
                            name=HOSTNAME + "." + self.processor.module,
                            volumes={
                                os.getcwd() + "/out": {"bind": "/tmp/", "mode": "rw"}
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
                        self.processor.container_image,
                        self.processor.container_version,
                        self.container,
                    )

                    logging.info(
                        "Installing repo inside container...%s",
                        self.processor.gitrepo.strip(),
                    )

                    # TODO: Only install repo if processor has one
                    # TODO: Install requirements.txt if processor has one
                    # Install the repo inside the container
                    res = self.container.exec_run(
                        "pip install -e git+" + self.processor.gitrepo.strip()
                    )

                    logging.info("OUTPUT: %s", res.output)

                    with open(f"{agent_cwd}/{self.processor.name}.pid", "w") as cfile:
                        cfile.write(str(self.container.short_id) + "\n")

                    with open(f"{agent_cwd}/containers.pid", "a") as cfile:
                        cfile.write(str(self.container.short_id) + "\n")
                    # Append container id to containers.pid

            logging.info("Worker starting session....")

            with self.get_session(self.database) as session:
                logging.info("Worker got session....")
                # session.refresh(self.processor)
                logging.info("================== WORKER PROCESSOR %s", self.processor)
                logging.info("Getting processor {}".format(self.processor.id))
                task_queues = []
                task_routes = {}

                logging.info("My processor is: {}".format(self.processor))
                logging.info("Processor sockets: {}".format(self.processor.sockets))

                _processor = (
                    session.query(ProcessorModel)
                    .filter_by(id=self.processor.id)
                    .first()
                )
                if _processor and _processor.sockets and len(_processor.sockets) > 0:
                    logging.info("Setting up sockets...")
                    for socket in _processor.sockets:
                        logging.info("Socket %s", socket)
                        if socket.queue:

                            # TODO: Use socket.task.name as the task name and _processor.module as the module
                            # For each socket task, use a queue named socket.queue.name+_processor.name+socket.task.name
                            # for example: queue1.proc1.some_task_A, queue1.proc1.some_task_B

                            # This queue is bound to a broadcast(fanout) exchange that delivers
                            # a message to all the connected queues however sending a task to
                            # this queue will deliver to this processor only
                            processor_path = (
                                socket.queue.name
                                + "."
                                + _processor.name.replace(" ", ".")
                            )

                            logging.info("Joining room %s", processor_path)
                            if processor_path not in queues:
                                queues += [processor_path]

                            processor_task = (
                                socket.queue.name
                                + "."
                                + _processor.name.replace(" ", ".")
                                + "."
                                + socket.task.name
                            )
                            processor_task2 = _processor.module + "." + socket.task.name

                            if processor_task not in queues:
                                # room = {'room': processor_task}
                                queues += [processor_task]

                            if processor_task2 not in queues:
                                queues += [processor_task2]

                            # This topic queue represents the broadcast fanout to all workers connected
                            # to it. Sending a task to this queue delivers to all connected workers
                            # queues += []

                            from kombu import Exchange, Queue, binding
                            from kombu.common import Broadcast

                            logging.debug(
                                "socket.queue.expires %s", socket.queue.expires
                            )

                            for processor_plug in socket.targetplugs:
                                """ PLUG ROUTING """
                                tkey = (
                                    processor_plug.source.queue.name
                                    + "."
                                    + self.processor.module
                                    + "."
                                    + processor_plug.source.task.name
                                )
                                tkey2 = (
                                    _processor.module
                                    + "."
                                    + processor_plug.source.task.name
                                )

                                # PLUG ROUTING
                                routing_key = processor_plug.queue.name + "." + self.processor.module + "." + socket.task.name

                                # PLUG ROUTING
                                plug_queue = KQueue(
                                    processor_plug.queue.name,
                                    Exchange(
                                        processor_plug.queue.name,
                                        type="direct",
                                    ),
                                    routing_key=routing_key,
                                    message_ttl=socket.queue.message_ttl,
                                    durable=socket.queue.durable,
                                    expires=socket.queue.expires,
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
                                    processor_plug.queue.name + "." + self.processor.module + "." + socket.task.name
                                ] = {
                                    "queue": processor_plug.queue.name,
                                    "exchange": [
                                        processor_plug.queue.name
                                    ],
                                }

                                # PLUG ROUTING
                                logging.info("ADDED ROUTE %s for %s",processor_plug.queue.name + "." + self.processor.module + "." + socket.task.name,
                                task_routes[
                                    processor_plug.queue.name + "." + self.processor.module + "." + socket.task.name
                                ])
                                logging.info("ADDED TARGET PLUG QUEUE %s", plug_queue)
                                task_queues += [plug_queue]


                            for processor_plug in socket.sourceplugs:
                                """ PLUG ROUTING """
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
                                routing_key = processor_plug.target.queue.name + "." + fix(self.processor.name) + "." + socket.task.name

                                # PLUG ROUTING
                                plug_queue = KQueue(
                                    processor_plug.target.queue.name,
                                    Exchange(
                                        processor_plug.target.queue.name,
                                        type="direct",
                                    ),
                                    routing_key=routing_key,
                                    message_ttl=socket.queue.message_ttl,
                                    durable=socket.queue.durable,
                                    expires=socket.queue.expires,
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
                                    processor_plug.target.queue.name + "." + self.processor.module + "." + socket.task.name
                                ] = {
                                    "queue": processor_plug.target.queue.name,
                                    "exchange": [
                                        processor_plug.target.queue.name
                                    ],
                                }

                                # PLUG ROUTING
                                logging.info("ADDED ROUTE %s for %s",processor_plug.target.queue.name + "." + self.processor.module + "." + socket.task.name,
                                task_routes[
                                    processor_plug.target.queue.name + "." + self.processor.module + "." + socket.task.name
                                ])
                                logging.info("ADDED SOURCE PLUG QUEUE %s", plug_queue)
                                task_queues += [plug_queue]

                            task_queues += [
                                KQueue(
                                    socket.queue.name
                                    + "."
                                    + fix(self.processor.name)
                                    + "."
                                    + socket.task.name,
                                    Exchange(
                                        socket.queue.name
                                        + "."
                                        + fix(self.processor.name)
                                        + "."
                                        + socket.task.name,
                                        type="direct",
                                    ),
                                    routing_key=socket.queue.name
                                    + "."
                                    + fix(self.processor.name)
                                    + "."
                                    + socket.task.name,
                                    message_ttl=socket.queue.message_ttl,
                                    durable=socket.queue.durable,
                                    expires=socket.queue.expires,
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
                                    self.processor.module + "." + socket.task.name,
                                    Exchange(
                                        socket.queue.name
                                        + "."
                                        + fix(self.processor.name)
                                        + "."
                                        + socket.task.name,
                                        type="direct",
                                    ),
                                    routing_key=self.processor.module
                                    + "."
                                    + socket.task.name,
                                    message_ttl=socket.queue.message_ttl,
                                    durable=socket.queue.durable,
                                    expires=socket.queue.expires,
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
                                    socket.queue.name
                                    + "."
                                    + fix(self.processor.name)
                                    + "."
                                    + socket.task.name,
                                    Exchange(
                                        socket.queue.name + ".topic", type="fanout"
                                    ),
                                    routing_key=socket.queue.name + ".topic",
                                    message_ttl=socket.queue.message_ttl,
                                    durable=socket.queue.durable,
                                    expires=socket.queue.expires,
                                    # TODO: These attributes need to come from Queue model
                                    queue_arguments={
                                        "x-message-ttl": 30000,
                                        "x-expires": 300,
                                    },
                                )
                            ]
                            task_routes[
                                self.processor.module + "." + socket.task.name
                            ] = {
                                "queue": socket.queue.name,
                                "exchange": [
                                    socket.queue.name + ".topic",
                                    socket.queue.name,
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

                logging.info(
                    "Creating celery worker %s %s %s deployment %s",
                    self.processor.name + "@" + HOSTNAME,
                    self.backend,
                    self.broker,
                    self.deployment.cpus,
                )

                worker = None
                try:
                    worker = app.Worker(
                        hostname=self.hostname
                        + "."
                        + _processor.name
                        + "."
                        + self.deployment.name
                        + "@"
                        + self.agent.hostname,
                        backend=self.backend,
                        broker=self.broker,
                        beat=_processor.beat,
                        uid="pyfi",
                        without_mingle=True,
                        without_gossip=True,
                        concurrency=int(self.deployment.cpus),
                    )
                    worker.concurrency = int(self.deployment.cpus)
                except Exception as ex:
                    logging.error(ex)

                logging.info("Created celery worker")

                # Find existing model first
                try:
                    logging.info(
                        "Creating workerModel with worker dir %s", self.workdir
                    )

                    if self.deployment.worker:
                        workerModel = self.deployment.worker
                    else:
                        workerModel = (
                            session.query(WorkerModel)
                            .filter_by(
                                name=HOSTNAME + ".agent." + _processor.name + ".worker"
                            )
                            .first()
                        )

                    if workerModel is None:
                        workerModel = WorkerModel(
                            name=HOSTNAME + ".agent." + _processor.name + ".worker",
                            concurrency=int(self.deployment.cpus),
                            status="ready",
                            backend=self.backend,
                            processor=_processor,
                            broker=self.broker,
                            workerdir=self.workdir,
                            agent_id=self.agent.id,
                            hostname=HOSTNAME,
                            requested_status="start",
                        )

                        logging.info("Created workerModel")
                        session.add(workerModel)

                    workerModel.workerdir = self.workdir
                    # Attach worker to deployment
                    self.deployment.worker = workerModel
                    self.deployment.worker.hostname = HOSTNAME
                    workerModel.deployment = self.deployment
                    workerModel.port = self.port
                    session.commit()

                except Exception as ex:
                    logging.error(ex)

                logging.info("Checking beat")
                if self.processor.beat:
                    logging.info("Has beat")
                    worker.app.conf.beat_schedule = {}

                    for socket in self.processor.sockets:
                        if socket.interval <= 0:
                            continue

                        # TODO: QUEUENAME
                        tkey = (
                            socket.queue.name
                            + "."
                            + fix(self.processor.name)
                            + "."
                            + socket.task.name
                        )

                        worker_queue = KQueue(
                            tkey,
                            Exchange(socket.queue.name, type="direct"),
                            routing_key=tkey,
                            message_ttl=socket.queue.message_ttl,
                            durable=socket.queue.durable,
                            expires=socket.queue.expires,
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

                sys.path.append(os.getcwd())

                logging.info("Setting worker")
                setattr(builtins, "worker", worker)

                logging.debug("CWD %s", os.getcwd())

                logging.info("Importing processor module")
                module = importlib.import_module(_processor.module)

                _plugs = {}

                logging.info("Initializing plugs")
                for plug in _processor.plugs:
                    _plugs[plug.queue.name] = []

                logging.info("Configuring sockets")
                if _processor and _processor.sockets and len(_processor.sockets) > 0:
                    for socket in _processor.sockets:

                        if socket.scheduled:
                            try:
                                if socket.schedule_type == "CRON":
                                    print("ADDING CRON JOB TYPE")

                                elif socket.schedule_type == "INTERVAL":
                                    logging.info(
                                        "Found INTERVAL schedule for socket: %s", socket
                                    )
                                    if socket.name not in self.jobs:
                                        logging.info("Adding job-> %s", socket.name)
                                        plug = None
                                        for plug in _processor.plugs:
                                            if plug.target.name == socket.name:
                                                break

                                        if plug is None:
                                            logging.error("Job plug is NONE")
                                        else:
                                            # execute sql to get jobs
                                            found = False or socket.interval <= 0

                                            if not found:
                                                # Ensure job id matches socket so it can be related
                                                # Maybe this shouldn't use a plug
                                                try:
                                                    logging.info(
                                                        "Adding job %s with interval %s",
                                                        dispatcher,
                                                        socket.interval,
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
                                                        logging.debug(
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
                                                            socket.interval,
                                                            (
                                                                _processor,
                                                                plug,
                                                                "message",
                                                                session,
                                                                socket,
                                                            ),
                                                        ),
                                                    )
                                                    job.start()
                                                    # scheduler.add_job(dispatcher, 'interval', (self.processor, plug, "message", self.dburi, socket), jobstore='default',
                                                    #                    misfire_grace_time=60, coalesce=True, max_instances=1, seconds=socket.interval, id=self.processor.name+plug.name, )
                                                    logging.info(
                                                        "Scheduled socket %s",
                                                        socket.name,
                                                    )
                                                except:
                                                    logging.info(
                                                        "Job %s already scheduled.",
                                                        socket.name,
                                                    )

                            except:
                                import traceback

                                print(traceback.format_exc())
                                logging.info(
                                    "Already scheduled this socket %s", socket.name
                                )

                        logging.info("Socket task %s", socket.task)
                        if socket.task.code and not socket.task.endpoint:
                            # We have custom code for this task
                            # Add the task.code to the loaded module
                            # The task.code must have the named function
                            # contained in socket.task.name

                            # Inject the code into the module.
                            # The module originates in the mounted git repo
                            # So the task code is like a "mixin"
                            logging.debug("TASK CODE: %s", socket.task.code)
                            exec(socket.task.code, module.__dict__)
                        else:
                            logging.info("NO TASK CODE")

                        # Get the function from the loaded module
                        _func = getattr(module, socket.task.name)

                        logging.info(
                            "TASK SOURCE: %s %s %s",
                            socket.task.id,
                            socket.task,
                            socket.task.source,
                        )
                        _source = inspect.getsource(_func)
                        # session.merge(socket)
                        session.add(socket.task)
                        socket.task.source = _source
                        logging.info(
                            "Updated source for %s %s %s",
                            socket.task.id,
                            socket.task,
                            socket.task.source,
                        )
                        session.commit()
                        logging.info(
                            "TASK SOURCE:-> %s %s %s",
                            socket.task.id,
                            socket.task,
                            socket.task.source,
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

                            logging.info("WRAPPED FUNCTION INVOKE %s", socket.task)
                            logging.info("ARGS: %s, KWARGS: %s", args, kwargs)

                            taskid = kwargs["myid"]

                            _kwargs = kwargs["kwargs"] if "kwargs" in kwargs else None

                            if "argument" in kwargs:
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
                                for arg in socket.task.arguments:
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
                            _call = 'execute_function("{}", "{}", "{}")'.format(
                                taskid, socket.task.module, socket.task.name
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

                                    if _processor.detached:
                                        # Run command inside self.container passing in task id, module and function
                                        pythoncmd = "python /tmp/" + taskid + ".py"
                                        logging.info("Invoking %s", pythoncmd)

                                        logging.info("CONTAINER RUN: %s", pythoncmd)

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
                                        logging.info("OUT PATH %s", "out/" + taskid)
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
                                        logging.info("%s OUTPUT: %s", _func, output)
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
                                logging.info("Invoking function %s", args)

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

                                    if _processor.detached:
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
                                        logging.info("Invoking %s", pythoncmd)

                                        logging.info("CONTAINER RUN: %s", pythoncmd)
                                        res = self.container.exec_run(pythoncmd)
                                        output = res.output.decode("utf-8")
                                        logging.info("OUTPUT: %s", output)
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
                                    # from io import StringIO # Python3 use: from io import StringIO
                                    # old_stdout = sys.stdout
                                    # sys.stdout = mystdout = StringIO()
                                    import io
                                    from contextlib import redirect_stdout

                                    try:
                                        # TODO: Get stdout, stderr
                                        result = None
                                        # blah blah lots of code ...
                                        with io.StringIO() as buf, redirect_stdout(buf):
                                            result = _func(*args)
                                            output = buf.getvalue()
                                            logging.info("%s OUTPUT: %s", _func, output)
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
                                        print("_R EXCEPTION", _r)
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
                            name=_processor.module + "." + socket.task.name,
                            retries=_processor.retries,
                        )

                        """
                        Everything that hosts and runs user code is a processor, but there are different types.
                        Each type handles the meta invocation a bit different.

                        if processor is a gate
                            func = self.celery.task(gate_function, name=self.processor.module +
                            '.' + socket.task.name, retries=self.processor.retries)

                        if processor is a router
                            func = self.celery.task(router_function, name=self.processor.module +
                            '.' + socket.task.name, retries=self.processor.retries)
                        """

                        @task_prerun.connect()
                        def pyfi_task_prerun(
                            sender=None, task=None, task_id=None, *args, **kwargs
                        ):
                            """Update args and kwargs before sending to task. Other bookeeping"""
                            from datetime import datetime

                            # PRERUN_CONDITION.acquire()
                            try:
                                print("prerun TASK: ", type(task), task, kwargs)

                                if sender.__name__ == "enqueue":
                                    return

                                _function_name = task.name.rsplit(".")[-1:]

                                if "tracking" not in kwargs["kwargs"]:
                                    tracking = str(uuid4())
                                    kwargs["kwargs"]["tracking"] = tracking

                                kwargs["kwargs"]["prerun"] = str(datetime.now())
                                print(
                                    "KWARGS:",
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

                                logging.info("Waiting on PRERUN REPLY")
                                response = self.prerun_queue.get()
                                logging.info("GOT PRERUN QUEUE MESSAGE %s", response)
                                if "error" in response:
                                    logging.error(response["error"])
                                else:
                                    kwargs["kwargs"].update(response)
                                kwargs["kwargs"]["output"] = {}

                                logging.info("PRERUN QUEUE: %s", response)
                                logging.info("PRERUN KWARGS IS NOW: %s", kwargs)

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
                            logging.info("Task SUCCESS: %s", sender)
                            # Store task run data
                            pass

                        @task_failure.connect()
                        def pyfi_task_failure(sender=None, **kwargs):
                            # Store task run data
                            logging.info("Task FAILURE: %s %s", sender, kwargs)

                        @task_internal_error.connect()
                        def pyfi_task_internal_error(sender=None, **kwargs):
                            # Store task run data
                            pass

                        @task_received.connect()
                        def pyfi_task_received(sender=None, request=None, **kwargs):
                            logging.info(
                                "Task RECEIVED REQUEST %s %s %s",
                                request.id,
                                sender,
                                request.name,
                            )

                            _function_name = request.name.rsplit(".")[-1:]
                            logging.info("Task Request Parent %s", request.parent_id)
                            from datetime import datetime

                            sender = request.task_name.rsplit(".")[-1]
                            print("RECEIVED SENDER:", sender)

                            if sender == "enqueue":
                                return

                            tracking = str(uuid4())
                            print("KWARGS", kwargs)
                            print(
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
                            self.main_queue.put(
                                {
                                    "signal": "received",
                                    "sender": _function_name[0],
                                    "kwargs": {"tracking": tracking},
                                    "request": request.id,
                                    "taskparent": request.parent_id,
                                    "taskid": request.id,
                                }
                            )
                            print("PUT RECEIVED KWARGS on queue")

                            # Wait for reply
                            print("WAITING ON received_queue")
                            _kwargs = self.received_queue.get()
                            kwargs.update(_kwargs)
                            print("GOT RECEIVED REPLY ", _kwargs)
                            print("New KWARGS ARE:", kwargs)

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
                            logging.info("TASK POSTRUN ARGS: %s", args)
                            logging.info("TASK POSTRUN RETVAL: %s", retval)

                            logging.info(
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
                            logging.info("POSTRUN PUTTING ON main_queue %s", postrun)
                            self.main_queue.put(postrun)
                            logging.info("POSTRUN DONE PUTTING ON main_queue")

                logging.info("Starting scheduler...")
                scheduler.start()
                logging.info("Starting worker...")
                worker.start()

        if self.worker:
            logging.debug(
                "Preparing worker %s %s %s %s %s",
                self.worker.name,
                self.processor.plugs,
                self.backend,
                self.broker,
                self.worker.processor.module,
            )

        """ Install gitrepo and build virtualenv """
        if self.processor.commit and self.skipvenv:
            if self.processor.commit:
                os.system("git checkout {}".format(self.processor.commit))

        if self.processor.gitrepo and not self.skipvenv:

            if self.usecontainer:
                """Launch pyfi:latest container passing in variables and gitrepo. Maintain reference to launched container"""
                raise NotImplementedError
            else:
                """Build our virtualenv and import the gitrepo for the processor"""
                logging.debug(
                    "git clone -b {} --single-branch {} git".format(
                        self.processor.branch, self.processor.gitrepo
                    )
                )

                # if not 'clean' and path for self.worker.workdir exists
                # then move to that directory
                # Create git directory and pull the remote repo

                if self.worker:
                    logging.info("Worker directory: %s", self.worker.workerdir)

                logging.info("Current directory: %s", os.getcwd())

                if (
                    self.worker
                    and self.worker.workerdir
                    and os.path.exists(self.worker.workerdir)
                    and os.path.exists(self.worker.workerdir + "/git")
                ):
                    logging.info(
                        "Changing to existing work directory %s", self.worker.workerdir
                    )
                    os.chdir(self.worker.workerdir + "/git")
                    os.system("git config --get remote.origin.url")
                    os.system("git config pull.rebase false")
                    logging.info("Pulling update from git")
                    os.system("git pull")
                else:
                    """Clone gitrepo. Retry after 3 seconds if failure"""
                    count = 1
                    logging.info("cwd is %s", os.getcwd())
                    logging.info("workdir is %s", self.workdir)

                    if not os.path.exists(self.workdir):
                        os.makedirs(self.workdir)
                    else:
                        os.chdir(self.workdir)

                    while True:
                        """Try 5 times to clone repo successfully"""
                        if count >= 5:
                            break
                        try:
                            logging.info(
                                "git clone -b {} --single-branch {} git".format(
                                    self.processor.branch,
                                    self.processor.gitrepo.split("#")[0],
                                )
                            )
                            os.system(
                                "git clone -b {} --single-branch {} git".format(
                                    self.processor.branch,
                                    self.processor.gitrepo.split("#")[0],
                                )
                            )
                            sys.path.append(self.workdir + "/git")
                            os.chdir("git")
                            os.system("git config credential.helper store")
                            break
                        except Exception as ex:
                            logging.error(ex)
                            time.sleep(3)
                            count += 1

                # Create or update venv
                from virtualenvapi.manage import VirtualEnvironment

                # If not using a container, then build the virtualenv
                if not os.path.exists("venv"):

                    logging.info("Building virtualenv...in %s", os.getcwd())
                    env = VirtualEnvironment(
                        "venv", python=sys.executable, system_site_packages=True
                    )  # inside git directory

                    login = os.environ["GIT_LOGIN"]

                    # Install pyfi
                    # TODO: Make this URL a setting so it can be overridden
                    env.install("psycopg2")
                    env.install("pymongo")
                    env.install("-e git+" + login + "/radiantone/pyfi-private#egg=pyfi")

                    if not self.processor.use_container:
                        """If we are not running the processor tasks in a container, then load it into the venv"""
                        try:
                            env.install("-e git+" + self.processor.gitrepo.strip())
                        except:
                            import traceback

                            print(traceback.format_exc())
                            logging.error(
                                "Could not install %s", self.processor.gitrepo.strip()
                            )

            if self.processor.commit and not self.processor.gittag:
                os.system("git checkout {}".format(self.processor.commit))

            if self.processor.gittag:
                os.system("git checkout {}".format(self.processor.gittag))

        # Sometimes we just want to recreate the setup
        if not start:
            return

        from threading import Thread

        """ Start worker process"""
        worker_process = self.worker_process = Thread(
            target=worker_proc,
            name="worker_proc",
            args=(self.celery, self.queue, self.dburi),
        )

        worker_process.app = self.celery
        worker_process.daemon = True
        worker_process.start()
        logging.info("worker_process started...")

        self.process = worker_process

        def emit_messages():
            """Get messages off queue and emit to pubsub server"""
            redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))
            from setproctitle import setproctitle

            setproctitle("pyfi worker::emit_messages")
            while True:

                try:
                    message = self.queue.get()
                    logging.info("Emitting message %s %s", message[1]["room"], message)
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

        emit_process = self.emit_process = Thread(
            target=emit_messages, name="emit_messages"
        )
        emit_process.daemon = True
        emit_process.start()
        logging.info("emit_messages started...")

        def web_server():
            from setproctitle import setproctitle

            try:
                setproctitle("pyfi worker::web_server")
                logging.info("Starting worker web server on %s", self.port)
                bjoern.run(app, "0.0.0.0", self.port)
            except Exception as ex:
                logging.error(ex)
                logging.info("worker web_server: exiting...")

        webserver = Process(target=web_server, daemon=True)
        webserver.start()

        return worker_process

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
        logging.info("Terminating worker")

        process = psutil.Process(os.getpid())

        for child in process.children(recursive=True):
            try:
                child.kill()
            except:
                pass

        # process.kill()
        # process.terminate()

        # os.killpg(os.getpgid(process.pid), 15)
        # os.kill(process.pid, signal.SIGKILL)

        logging.debug("Finishing.")

        try:
            self.process.join()
        except:
            pass

        if os.path.exists(self.workdir):
            logging.info("Removing working directory %s", self.workdir)
            shutil.rmtree(self.workdir)

        logging.info("Done killing worker.")


@app.route("/")
def hello():
    import json

    return json.dumps({"status": "green"})
