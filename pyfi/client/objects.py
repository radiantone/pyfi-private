"""

proc1 = Processor(queue='pyfi.queue1.proc1', module='pyfi.processors.sample', name='proc1')
socket = Socket(queue='pyfi.queue1', task='do_something')
proc1.sockets += [socket]

"""
import os
import configparser
import platform

from celery import Celery
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


class Socket(Base):
    """
    Docstring
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.name = kwargs['name']
        self.queuename = kwargs['queue']['name']
        self.processor = kwargs['processor']
        self.task = kwargs['task']

        task = self.session.query(
            TaskModel).filter_by(name=self.task).first()
        if task is None:
            task = TaskModel(name=self.task)

        self.socket = self.session.query(
            SocketModel).filter_by(name=self.name).first()

        self.queue = Queue(name=self.queuename)

        self.session.add(self.processor.processor)

        if self.socket is not None:
            self.session.add(self.socket)
            self.session.add(task)
            self.socket.task = task
        else:
            self.socket = SocketModel(name=self.name, processor_id=self.processor.processor.id, requested_status='ready',
                                      status='ready')

            self.session.add(task)
            self.socket.task = task
            self.session.add(self.socket)
            self.session.commit()
            self.session.refresh(
                self.socket)

        self.key = self.queuename+self.socket.task.name

        try:
            self.database.session.add(self.queue.queue)
        except:
            pass

        if self.socket.queue is None:
            print("Adding queue", self.queue.queue.name)
            self.socket.queue = self.queue.queue
            self.session.add(self.queue.queue)
            self.session.add(self.socket)

        self.processor.sockets += self.socket
        self.session.commit()

        self.queue = KQueue(
            self.queuename+'.'+self.processor.processor.name+'.'+self.socket.task.name,
            Exchange(self.queuename, type='direct'),
            routing_key=self.key,
            expires=30,

            # socket.queue.message_ttl
            # socket.queue.expires
            queue_arguments={
                'x-message-ttl': 30000,
                'x-expires': 30000}
        )

        self.processor.app.conf.task_routes = {
            self.key: {
                'queue': self.queue,
                'exchange': self.queuename
            }
        }

    def __call__(self, *args, **kwargs):

        # socket.queue.message_ttl
        # socket.queue.expires
        kwargs['x-expires'] = 30000
        self.session.add(self.socket)
        self.session.refresh(
            self.socket)
        print("called", self.processor.processor.module +
              '.'+self.socket.task.name, args, self.queuename)
        qname = self.queuename+'.'+self.processor.processor.name+'.'+self.socket.task.name
        return self.processor.app.signature(self.processor.processor.module+'.'+self.socket.task.name, args=args, queue=self.queue, kwargs=kwargs).delay()


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
                print("IADD1 ", type(arg.queue.name))

                if isinstance(arg, Socket):
                    socket = self.database.session.query(
                        SocketModel).filter_by(name=arg.name).first()
                else:
                    socket = arg

                print("IADD2 ", type(socket.queue.name))
                self.session.add(self.processor)
                socket.processor_id = self.processor.id
                self.processor.sockets += [socket]
                print("SELF PROC SOCKETS", self.processor.sockets)
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

    def __init__(self, queue=None, name=None, gitrepo=None, branch=None, module=None, concurrency=3, commit=None, beat=False):

        super().__init__()

        from kombu.common import Broadcast

        '''
        Load the processor by name and match the queue by name, then use
        the queue object to create the kombu Queue() class so it matches
        '''

        self.queue = queue
        self.name = name

        self.processor = self.session.query(
            ProcessorModel).filter_by(name=name).first()
        # Collection for socket relations

        if self.processor is None:
            # Create it
            print("Creating processor")
            self.processor = ProcessorModel(
                status='ready', hostname=platform.node(), retries=10, gitrepo=gitrepo, branch=branch, beat=beat, commit=commit, concurrency=concurrency, requested_status='update', name=name, module=module)

        self.sockets = Sockets(self.database, self.processor)

        backend = CONFIG.get('backend', 'uri')
        broker = CONFIG.get('broker', 'uri')
        self.app = Celery(backend=backend, broker=broker)
        # Get celery values from pyfi.ini

        # self.app.config_from_object(Config)

        # If the queues are on the sockets, is this even needed?
        if queue:
            if queue.find('topic') > -1:
                self.app.conf.task_queues = (
                    Broadcast(queue, queue_arguments={
                        'x-message-ttl': 3000,
                        'x-expires': 30}),)

            else:
                # Use peristent queue object from database to populate
                # values here to avoid error messages
                self.queue = queue = KQueue(
                    queue,
                    Exchange(queue, type='direct'),
                    routing_key=name,
                    expires=30,
                    queue_arguments={
                        'x-message-ttl': 30000,
                        'x-expires': 30}
                )

            self.app.conf.task_routes = {
                name: {
                    'queue': queue,
                    'exchange': queue
                }
            }

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
