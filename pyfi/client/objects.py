"""
API objects

proc1 = Processor(queue='pyfi.queue1.proc1', module='ext.processors.sample', name='proc1')
socket = Socket(queue='pyfi.queue1', task='do_something')
proc1.sockets += [socket]

"""
import logging

logger = logging.getLogger(__name__)

import configparser
from pathlib import Path
from typing import List

from celery import Celery
from kombu import Exchange
from kombu import Queue as KQueue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyfi.db.model import (
    AgentModel,
    ArgumentModel,
    DeploymentModel,
    NetworkModel,
    NodeModel,
    PlugModel,
    ProcessorModel,
    QueueModel,
    SchedulerModel,
    SocketModel,
    TaskModel,
    WorkerModel,
)

# from pyfi.server.api import app

CONFIG = configparser.ConfigParser()
HOME = str(Path.home())

ini = HOME + "/pyfi.ini"

CONFIG.read(ini)


class Registry(dict):
    """Singleton that holds all the in-memory references during network creation"""

    pass


registry = Registry()

# serialization.register_pickle()
# serialization.enable_insecure_serializers()


class SocketNotFoundException(Exception):
    pass


class Base:
    """
    Docstring
    """

    database = None
    session = None

    db = CONFIG.get("database", "uri")
    backend = CONFIG.get("backend", "uri")
    broker = CONFIG.get("broker", "uri")
    database = create_engine(db)
    session = sessionmaker(bind=database)()
    setattr(database, "session", session)

    def __init__(self):
        pass


class Work(Base):
    """A descripion of a task or scheduled task submitted for execution"""

    # Some users may only have permission to create Work objects and not
    # reference Sockets/Plugs directly
    pass


class Worker(Base):
    """
    Docstring
    """

    def __init__(self, name=None, hostname=None, processor=None, agent=None):
        super().__init__()

        name = hostname + processor.name + ".worker"
        self.worker = self.session.query(WorkerModel).filter_by(name=name).first()
        self.app = Celery(backend=self.backend, broker=self.broker)

        if self.worker is None:
            self.worker = _worker = WorkerModel(
                name=name,
                processor=processor,
                backend=self.backend,
                agent_id=agent.id,
                broker=self.broker,
                hostname=hostname,
            )

        self.session.add(self.worker)
        self.session.commit()


class Agent(Base):
    """
    Docstring
    """

    worker: Worker

    @classmethod
    def find(cls, name):
        return cls.session.query(AgentModel).filter_by(name=name).first()

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.agent = None

        self.name = kwargs["name"]
        self.hostname = kwargs["hostname"]
        self.node = kwargs["node"]

        self.agent = self.session.query(AgentModel).filter_by(name=self.name).first()

        if self.agent is None:
            self.agent = AgentModel(
                name=self.name, node_id=self.node.node.id, hostname=self.hostname
            )

        self.session.add(self.agent)
        self.session.commit()


class Node(Base):
    """
    Docstring
    """

    agent: Agent

    def __init__(self, name=None, hostname=None):
        super().__init__()

        self.node = self.session.query(NodeModel).filter_by(name=name).first()

        if self.node is None:
            self.node = _node = NodeModel(name=name, hostname=hostname)

        self.session.add(self.node)
        self.session.commit()


class Network(Base):
    """
    Docstring
    """

    nodes: List[Node] = []

    def __init__(self, name=None, user=None):
        super().__init__()

        self.network = self.session.query(NetworkModel).filter_by(name=name).first()

        if self.network is None:
            self.network = NetworkModel(name=name, user=user)

        self.session.add(self.network)
        self.session.commit()


class Task(Base):
    """
    Docstring
    """

    def __init__(self, name=None, module=None, repo=None, queue=None):
        super().__init__()

        self.app = Celery(backend=self.backend, broker=self.broker)
        self.task = self.session.query(TaskModel).filter_by(name=name).first()

        if self.task is None:
            self.task = _task = TaskModel(name=name, module=module, gitrepo=repo)

            # Add Argument objects ehre

            self.session.add(self.task)
            self.session.commit()
            # raise Exception(f"Task {name} does not exist.")

        self.name = module + "." + name

        self.queue = KQueue(
            queue["name"],
            Exchange(
                queue["name"], type=queue["type"], routing_key=module + "." + name
            ),
        )

    def __call__(self, *args, **kwargs):
        return self.app.signature(
            self.name,
            app=self.app,
            args=args,
            serializer="pickle",
            queue=self.queue,
            kwargs=kwargs,
        ).delay()


class Argument(Base):
    """
    Docstring
    """

    @classmethod
    def find(cls, name, task):
        return (
            cls.session.query(ArgumentModel)
            .join(TaskModel)
            .filter(
                ArgumentModel.name == name
                and TaskModel.name == task
                and ArgumentModel.task_id == TaskModel.id
            )
            .first()
        )


class Scheduler(Base):
    """
    Docstring
    """

    strategy = "BALANCED"

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.scheduler = None

        self.name = kwargs["name"]
        self.strategy = kwargs["strategy"]

        self.scheduler = (
            self.session.query(SchedulerModel).filter_by(name=self.name).first()
        )

        if self.scheduler is None:
            self.scheduler = SchedulerModel(name=self.name, strategy=self.strategy)
            self.session.add(self.scheduler)
            self.session.commit()
        else:
            self.session.add(self.scheduler)

    def __iadd__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, Node) or isinstance(arg, NodeModel):

                if isinstance(arg, Node):
                    pass
                else:
                    self.session.add(arg)
                    self.scheduler.nodes += [arg]


class Socket(Base):
    """
    Docstring
    """

    synchronized = False

    def __init__(self, *args, **kwargs):
        import importlib
        import inspect

        super().__init__()

        backend = CONFIG.get("backend", "uri")
        broker = CONFIG.get("broker", "uri")
        logging.debug("Socket: %s %s", backend, broker)
        self.app = Celery(backend=backend, broker=broker)

        from pyfi.util import config

        self.app.config_from_object(config)
        self.processor = None
        self.socket = None

        if "name" in kwargs:
            self.name = kwargs["name"]
        else:
            self.name = None

        interval = -1

        if "interval" in kwargs:
            interval = kwargs["interval"]

        if "queue" in kwargs:
            self.queuename = kwargs["queue"]["name"]
            # pass in x-expires, message-ttl
            self.queue = Queue(**kwargs["queue"])
            self.session.add(self.queue.queue)

        if "processor" in kwargs:
            self.processor = kwargs["processor"]
            self.session.add(self.processor.processor)

        if "sync" in kwargs:
            self.synchronized = kwargs["sync"]

        self.loadbalanced = False
        if "loadbalanced" in kwargs:
            self.loadbalanced = kwargs["loadbalanced"]

        if self.name:
            self.socket = (
                self.session.query(SocketModel).filter_by(name=self.name).first()
            )

        if self.socket and not self.processor:
            self.processor = Processor(id=self.socket.processor.id)

        if "task" in kwargs:
            taskname = kwargs["task"]
            modulename = kwargs["module"] if "module" in kwargs else None

            if type(taskname) is str:
                self.socket = (
                    self.session.query(SocketModel)
                    .join(TaskModel, SocketModel.task)
                    .filter(
                        TaskModel.name == taskname and TaskModel.module == modulename
                    )
                    .first()
                )
                logging.info(
                    "Socket from task %s and module %s: %s",
                    taskname,
                    modulename,
                    self.socket,
                )
                if self.socket:
                    self.processor = Processor(id=self.socket.processor.id)

                if modulename:
                    self.task = (
                        self.session.query(TaskModel)
                        .filter_by(name=taskname, module=modulename)
                        .first()
                    )
                else:
                    self.task = (
                        self.session.query(TaskModel).filter_by(name=taskname).first()
                    )

                if self.task is None:
                    self.task = TaskModel(name=taskname)

                if "code" in kwargs:
                    self.task.source = kwargs["source"]
                if "source" in kwargs:
                    self.task.source = kwargs["source"]

            if type(taskname) is TaskModel:
                self.task = taskname

            self.task.module = self.processor.processor.module
            self.task.gitrepo = self.processor.processor.gitrepo
            self.session.add(self.task)

        user = kwargs["user"]
        try:
            self.session.add(user)
        except:
            pass

        if "arguments" in kwargs and kwargs["arguments"]:

            _module = importlib.import_module(self.task.module)
            _function = getattr(_module, self.task.name)
            _signature = inspect.signature(_function)

            position = 0
            self.task.arguments = []

            for pname in _signature.parameters:
                param = _signature.parameters[pname]
                _argument = ArgumentModel(
                    name=param.name, position=position, user=user, kind=param.kind
                )
                self.session.add(_argument)
                self.task.arguments += [_argument]
                position += 1

        if self.socket is not None:

            if self.processor is None:
                self.processor = Processor(id=self.socket.processor_id)

            if self.socket.queue is None and self.queue is not None:
                self.socket.queue = self.queue.queue

            self.session.add(self.socket)

            if self.socket.task is None:
                self.socket.task = self.task
        else:
            scheduled = False
            schedule_type = "INTERVAL"

            if interval > 0:
                scheduled = True

            self.socket = SocketModel(
                name=self.name,
                user=user,
                user_id=user.id,
                scheduled=scheduled,
                schedule_type=schedule_type,
                interval=interval,
                processor_id=self.processor.processor.id,
                requested_status="ready",
                status="ready",
            )

            logger.debug("Creating new socket %s", self.name)
            self.session.add(self.task)
            self.socket.task = self.task
            self.socket.queue = self.queue.queue
            self.session.add(self.socket)
            self.session.commit()
            self.session.refresh(self.socket)

        self.key = (
            self.socket.queue.name
            + "."
            + self.processor.name
            + "."
            + self.socket.task.name
        )

        try:
            self.database.session.add(self.queue.queue)
        except:
            pass

        if self.socket.queue is None:
            self.socket.queue = self.queue.queue
            self.session.add(self.queue.queue)
            self.session.add(self.socket)

        self.processor.sockets += [self.socket]
        self.session.commit()

        self.kqueue = KQueue(
            self.key,
            Exchange(self.socket.queue.name, type="direct"),
            routing_key=self.key,
            message_ttl=self.socket.queue.message_ttl,
            durable=self.socket.queue.durable,
            expires=self.socket.queue.expires,
            # socket.queue.message_ttl
            # socket.queue.expires
            queue_arguments={"x-message-ttl": 30000, "x-expires": 300},
        )

        # For load balanced queue

        if self.loadbalanced:
            self.key = self.processor.processor.module + "." + self.socket.task.name
            self.kqueue = KQueue(
                self.key,
                # self.socket.queue.name+'.'+self.processor.name+'.'+self.socket.task.name
                Exchange(self.socket.queue.name, type="direct"),
                routing_key=self.key,
                message_ttl=self.socket.queue.message_ttl,
                durable=self.socket.queue.durable,
                expires=self.socket.queue.expires,
                # socket.queue.message_ttl
                # socket.queue.expires
                queue_arguments={"x-message-ttl": 30000, "x-expires": 300},
            )

        self.app.conf.task_routes = {
            self.key: {"queue": self.kqueue, "exchange": self.socket.queue.name}
        }

    def p(self, *args, **kwargs):
        """Partial method signature (not executed)"""
        logger.debug(
            "socket signature: %s",
            self.processor.processor.module + "." + self.socket.task.name,
        )
        try:
            return self.processor.app.signature(
                self.processor.processor.module + "." + self.socket.task.name,
                app=self.processor.app,
                args=args,
                serializer="pickle",
                queue=self.kqueue,
                kwargs=kwargs,
            )
        finally:
            self.processor.app.autodiscover_tasks(
                self.processor.processor.module + "." + self.socket.task.name
            )
            logger.debug("Autodiscover tasks")

    def delay(self, *args, **kwargs):
        """Execute this socket's task on the network"""
        # socket.queue.message_ttl
        # socket.queue.expires
        kwargs["x-expires"] = 300
        self.session.add(self.processor.processor)
        self.session.add(self.socket)
        self.session.refresh(self.socket)

        return self.p(args, kwargs).delay()

    def __call__(self, *args, **kwargs):
        import logging

        """"""
        # socket.queue.message_ttl
        # socket.queue.expires
        kwargs["x-expires"] = 300
        self.session.add(self.processor.processor)
        self.session.add(self.socket)
        self.session.refresh(self.socket)

        if not self.synchronized:
            logging.info(
                "Invoking task %s",
                self.processor.processor.module + "." + self.socket.task.name,
            )
            task_sig = (
                self.processor.app.signature(
                    self.processor.processor.module + "." + self.socket.task.name,
                    args=args,
                    queue=self.kqueue,
                    kwargs=kwargs,
                )
                .delay()
                .get()
            )

            # argument = {'name':'message','kind':3,'position':0}
            # task_sig_wait = self.processor.app.signature(
            #    self.processor.processor.module+'.'+self.socket.task.name+'.wait', args=(argument, args), queue=self.queue, kwargs=kwargs).delay().get()

            _task_sig = task_sig
            return _task_sig
        else:
            logger.debug("Invoking synchronized")
            # Follow paths from socket and build parallel/pipeline/chain/chord from aggregate sockets found
            # Then execute the parallel() object and wait for value, return that.
            self.processor.app.autodiscover_tasks(
                self.processor.processor.module + "." + self.socket.task.name
            )
            logger.debug("Autodiscover tasks")

            return


class Plug(Base):
    """
    Docstring
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.name = kwargs["name"]

        self.plug = self.session.query(PlugModel).filter_by(name=self.name).first()

        user = kwargs["user"]

        if self.plug is None:

            if "queue" in kwargs:
                self.queuename = kwargs["queue"]["name"]

            self.source = kwargs["source"]
            self.target = kwargs["target"]
            self.processor = kwargs["processor"]

            self.queue = Queue(name=self.queuename)
            self.session.add(self.processor.processor)

            self.session.add(user)
            self.session.add(self.queue.queue)
            self.session.add(self.source.socket)
            self.session.add(self.target.socket)

            self.plug = PlugModel(
                name=self.name,
                user=user,
                user_id=user.id,
                source=self.source.socket,
                target=self.target.socket,
                queue=self.queue.queue,
                processor_id=self.processor.processor.id,
                requested_status="ready",
                status="ready",
            )

            self.source.socket.sourceplugs += [self.plug]
            self.target.socket.targetplugs += [self.plug]

            try:
                self.session.add(self.source.socket)
                self.session.add(self.target.socket)
            except:
                # May already be in session, so ignore
                pass

            self.plug.source = self.source.socket
            self.plug.target = self.target.socket

            self.processor.processor.plugs += [self.plug]
            # self.plug.sockets += [self.socket.socket]
            self.session.add(self.plug)
            self.session.commit()


class Sockets(Base):
    """
    Docstring
    """

    def __init__(self, database, processor):
        self.database = database
        self.processor = processor

    def __iadd__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, Socket) or isinstance(arg, SocketModel):

                if isinstance(arg, Socket):
                    # socket = self.database.session.query(
                    #    SocketModel).filter_by(name=arg.name).first()
                    socket = arg.socket
                else:
                    socket = arg

                self.session.add(self.processor)
                socket.processor_id = self.processor.id
                self.processor.sockets += [socket]

        return self


class Queue(Base):
    """
    Docstring
    """

    def __init__(self, name=None, message_ttl=300000, durable=True, expires=300):
        super().__init__()

        self.name = name
        self.message_ttl = message_ttl
        self.durable = durable
        self.expires = expires

        self.queue = self.session.query(QueueModel).filter_by(name=name).first()

        if self.queue is None:
            # message_ttl=message_ttl, durable=durable, expires=expires,
            self.queue = QueueModel(name=name, requested_status="ready", status="ready")

            self.queue.message_ttl = self.message_ttl
            self.queue.durable = self.durable
            self.queue.expires = self.expires
            self.session.add(self.queue)

        self.session.commit()
        # self.session.expunge(self.queue)
        # self.session.close()


class Deployment(Base):
    def __init__(self, name=None, hostname=None, worker=None, processor=None, cpus=0):
        self.processor = processor

        self.deployment = (
            self.database.session.query(DeploymentModel).filter_by(name=name).first()
        )

        if self.deployment is None:
            self.deployment = DeploymentModel(
                name=name,
                worker=worker,
                hostname=hostname,
                processor=processor,
                cpus=cpus,
            )
            self.session.add(self.deployment)
            self.session.commit()


class Processor(Base):
    """
    Provide simple wrapper to ProcessorModel and execution behavior methods
    e.g.  processor = Processor()
          processor.start()
          processor.stop()
          processor.update(...)

          processor(arg1, arg2)

    class will manage the database model and celery backend in one place whereas
    using the cli you can only manage the database model.
    """

    def __init__(
        self,
        hostname=None,
        id=None,
        name=None,
        user=None,
        gitrepo=None,
        branch=None,
        module=None,
        requested_status="ready",
        concurrency=None,
        agent=None,
        commit=None,
        beat=None,
    ):

        super().__init__()

        from pyfi.util import config

        """
        Load the processor by name and match the queue by name, then use
        the queue object to create the kombu Queue() class so it matches
        """

        if id is not None:
            self.id = id
            self.processor = (
                self.database.session.query(ProcessorModel).filter_by(id=id).first()
            )
            self.name = self.processor.name
        else:
            self.name = name
            self.processor = (
                self.database.session.query(ProcessorModel).filter_by(name=name).first()
            )
        # Collection for socket relations

        if self.processor is None:
            # Create it
            self.processor = ProcessorModel(
                status="ready",
                user_id=user.id,
                user=user,
                retries=10,
                gitrepo=gitrepo,
                branch=branch,
                beat=beat,
                commit=commit,
                concurrency=concurrency,
                requested_status=requested_status,
                name=name,
                module=module,
            )
            self.database.session.add(self.processor)
            # self.processor.hostname = platform.node()
            self.processor.concurrency = 3
            self.processor.commit = None
            self.processor.beat = False

        """
        if self.processor.worker is None:
            _name = hostname + ".agent." + self.processor.name + '.worker'
            logger.info("Creating worker %s on %s",
                         _name, self.processor.name)
            _worker = WorkerModel(
                name=_name, backend=self.backend, agent=agent, broker=self.broker, hostname=hostname)
            self.processor.worker = _worker
            self.database.session.add(_worker)
            self.database.session.commit()
            logger.info("   Worker: %s", self.processor.worker.name)
        """

        if concurrency is not None:
            # if self.processor.concurrency != concurrency:
            #    self.processor.requested_status = "update"
            self.processor.concurrency = concurrency

        if commit is not None:
            if self.processor.commit != commit:
                self.processor.requested_status = "update"
            self.processor.commit = commit

        if beat is not None:
            if self.processor.beat != beat:
                self.processor.requested_status = "update"
            self.processor.beat = beat

        self.database.session.add(self.processor)

        self.sockets = Sockets(self.database, self.processor)

        backend = CONFIG.get("backend", "uri")
        broker = CONFIG.get("broker", "uri")

        self.app = Celery(backend=backend, broker=broker)

        self.app.config_from_object(config)
        self.database.session.commit()
        registry[self.processor.id] = self  # Add myself to the memory registry

    def get(self):
        self.database.session.add(self.processor)
        return self

    def start(self):
        self.processor.requested_status = "start"
        self.database.session.add(self.processor)
        self.database.session.commit()

    def stop(self):
        self.processor.requested_status = "stopped"
        self.database.session.add(self.processor)
        self.database.session.commit()

    def add_socket(self, socket):
        pass
