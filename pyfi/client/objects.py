"""

proc1 = Processor(queue='pyfi.queue1.proc1', module='pyfi.processors.sample', name='proc1')
socket = Socket(queue='pyfi.queue1', task='do_something')
proc1.sockets += [socket]

"""
import os
import configparser
import platform

from celery import Celery, signature
from pyfi.config.celery import Config
from kombu import Exchange, Queue as KQueue, binding
from pathlib import Path
from sqlalchemy import create_engine, MetaData, literal_column
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from pyfi.server import app
from pyfi.db.model import SchedulerModel, UserModel, AgentModel, WorkerModel, PlugModel, SocketModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel


CONFIG = configparser.ConfigParser()
HOME = str(Path.home())
ini = HOME+"/pyfi.ini"

CONFIG.read(ini)


class Base:
    """
    Docstring
    """
    database = None
    session = None

    db = CONFIG.get('database', 'uri')
    database = create_engine(db)
    session = sessionmaker(bind=database)()
    database.session = session

    def __init__(self):
        pass


class Node(Base):
    pass


class Scheduler(Base):
    """
    Docstring
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.scheduler = None

        self.name = kwargs['name']

        self.scheduler = self.session.query(
            SchedulerModel).filter_by(name=self.name).first()

        if self.scheduler is None:
            self.scheduler = SchedulerModel(name=self.name)
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

    def __init__(self, *args, **kwargs):
        super().__init__()
        
        backend = CONFIG.get('backend', 'uri')
        broker = CONFIG.get('broker', 'uri')
        self.app = Celery(backend=backend, broker=broker)

        from pyfi.celery import config
        self.app.config_from_object(config)
        self.processor = None

        self.name = kwargs['name']

        interval = -1

        if 'interval' in kwargs:
            interval = kwargs['interval']

        if 'queue' in kwargs:
            self.queuename = kwargs['queue']['name']
            # pass in x-expires, message-ttl
            self.queue = Queue(**kwargs['queue'])
            self.session.add(self.queue.queue)

        if 'processor' in kwargs:
            self.processor = kwargs['processor']
            self.session.add(self.processor.processor)

        if 'task' in kwargs:
            taskname = kwargs['task']

            self.task = self.session.query(
                TaskModel).filter_by(name=taskname).first()

            if self.task is None:
                self.task = TaskModel(name=taskname)

            self.task.module = self.processor.processor.module
            self.task.gitrepo = self.processor.processor.gitrepo
            self.session.add(self.task)


        self.socket = self.session.query(
            SocketModel).filter_by(name=self.name).first()

        if self.socket is not None:
            if self.socket.queue is None and self.queue is not None:
                self.socket.queue = self.queue.queue
            self.session.add(self.socket)
            if self.socket.task is None:
                self.socket.task = self.task
        else:
            self.socket = SocketModel(name=self.name, interval=interval, processor_id=self.processor.processor.id, requested_status='ready',
                                      status='ready')

            self.session.add(self.task)
            self.socket.task = self.task
            self.socket.queue = self.queue.queue
            self.session.add(self.socket)
            self.session.commit()
            self.session.refresh(
                self.socket)

        if self.processor is None:
            self.processor = Processor(id=self.socket.processor_id)

        self.key = self.socket.queue.name+'.'+self.processor.name+'.'+self.socket.task.name

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

        self.queue = KQueue(
            self.key,
            Exchange(self.socket.queue.name, type='direct'),
            routing_key=self.key,
            message_ttl=self.socket.queue.message_ttl,
            durable=self.socket.queue.durable,
            expires=self.socket.queue.expires,
            # socket.queue.message_ttl
            # socket.queue.expires
            queue_arguments={
                'x-message-ttl': 30000,
                'x-expires': 300}
        )

        self.app.conf.task_routes = {
            self.key: {
                'queue': self.queue,
                'exchange': self.socket.queue.name
            }
        }

    def p(self, *args, **kwargs):
        return self.processor.app.signature(self.processor.processor.module+'.'+self.socket.task.name, app=self.processor.app, args=args, serializer='pickle', queue=self.queue, kwargs=kwargs)

    def delay(self, *args, **kwargs):

        # socket.queue.message_ttl
        # socket.queue.expires
        kwargs['x-expires'] = 300
        self.session.add(self.processor.processor)
        self.session.add(self.socket)
        self.session.refresh(
            self.socket)

        return self.p(args,kwargs).delay()

    def __call__(self, *args, **kwargs):

        # socket.queue.message_ttl
        # socket.queue.expires
        kwargs['x-expires'] = 300
        self.session.add(self.processor.processor)
        self.session.add(self.socket)
        self.session.refresh(
            self.socket)

        return self.processor.app.signature(self.processor.processor.module+'.'+self.socket.task.name, args=args, queue=self.queue, kwargs=kwargs).delay().get()


class Plug(Base):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.name = kwargs['name']
        self.queuename = kwargs['queue']['name']
        self.source = kwargs['source']
        self.target = kwargs['target']
        self.processor = kwargs['processor']

        self.queue = Queue(name=self.queuename)
        self.session.add(self.processor.processor)

        self.plug = self.session.query(
            PlugModel).filter_by(name=self.name).first()

        if not self.plug:
            self.plug = PlugModel(name=self.name, queue=self.queue.queue, processor_id=self.processor.processor.id, requested_status='ready', status='ready')

        self.source.socket.sourceplugs += [self.plug.source]
        self.source.socket.targetplugs += [self.plug.target]

        self.session.add(self.source.socket)
        self.session.add(self.target.socket)
        self.plug.source = self.source.socket
        self.plug.target = self.target.socket
        #self.plug.sockets += [self.socket.socket]
        self.session.add(self.plug)
        self.processor.processor.plugs += [self.plug]
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
                    #socket = self.database.session.query(
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

    def __init__(self, name=None):
        super().__init__()

        self.name = name

        self.queue = self.session.query(
            QueueModel).filter_by(name=name).first()

        if self.queue is None:
            self.queue = QueueModel(name=name, requested_status='ready',
                                    status='ready')
            self.database.session.add(self.queue)
            self.database.session.commit()

        self.database.session.close()


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

    def __init__(self, hostname=platform.node(),id=None, name=None, gitrepo=None, branch=None, module=None, concurrency=3, commit=None, beat=False):

        super().__init__()

        from kombu.common import Broadcast

        '''
        Load the processor by name and match the queue by name, then use
        the queue object to create the kombu Queue() class so it matches
        '''


        if id is not None:
            self.id = id
            self.processor = self.session.query(
                ProcessorModel).filter_by(id=id).first()
            self.name = self.processor.name
        else:
            self.name = name
            self.processor = self.session.query(
                ProcessorModel).filter_by(name=name).first()
        # Collection for socket relations

        if self.processor is None:
            # Create it
            self.processor = ProcessorModel(
                status='ready', hostname=hostname, retries=10, gitrepo=gitrepo, branch=branch, beat=beat, commit=commit, concurrency=concurrency, requested_status='update', name=name, module=module)

        self.sockets = Sockets(self.database, self.processor)

        backend = CONFIG.get('backend', 'uri')
        broker = CONFIG.get('broker', 'uri')

        self.app = Celery(backend=backend, broker=broker)

        from pyfi.celery import config
        self.app.config_from_object(config)
        self.database.session.add(self.processor)
        self.database.session.commit()

    def start(self):
        self.processor.requested_status = 'start'
        self.database.session.add(self.processor)
        self.database.session.commit()

    def stop(self):
        self.processor.requested_status = 'stopped'
        self.database.session.add(self.processor)
        self.database.session.commit()

    def add_socket(self, socket):
        pass
