"""
Agent workerclass. Primary task/code execution context for processors
"""
import logging
import shutil
import os
import sys
import psutil
import signal
import configparser
from pathlib import Path

from multiprocessing import Condition, Queue
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyfi.db.model import UserModel, AgentModel, WorkerModel, PlugModel, SocketModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel
from pyfi.processor import Processor

from celery import Celery
from celery.signals import worker_process_init, after_task_publish, task_success, task_prerun, task_postrun, task_failure, task_internal_error, task_received
from kombu import Exchange, Queue as KQueue

from celery.signals import setup_logging


@setup_logging.connect
def setup_celery_logging(**kwargs):
    logging.debug("DISABLE LOGGING SETUP")
    pass

import socketio

home = str(Path.home())
CONFIG = configparser.ConfigParser()

events_server = os.environ['EVENTS']
lock = Condition()
queue = Queue()

global processes
processes = []


def shutdown(*args):
    for process in processes:
        logging.info("Terminating %s", process.pid)
        os.kill(process.pid, signal.SIGKILL)
        process.terminate()

    exit(0)


signal.signal(signal.SIGINT, shutdown)


class Worker:
    """
    A worker is a celery worker with a processor module loaded and represents a single processor
    """

    def __init__(self, processor, workdir, pool=4, database=None, backend='redis://localhost', celeryconfig=None, broker='pyamqp://localhost'):
        """
        """
        from pyfi.db.model import Base

        self.processor = processor
        self.worker = processor.worker
        self.backend = backend
        self.broker = broker
        self.workdir = workdir
        self.dburi = database

        self.database = create_engine(self.dburi)
        self.session = sessionmaker(bind=self.database)()
        self.database.session = self.session
        self.pool = pool

        if os.path.exists(home+"/pyfi.ini"):
            CONFIG.read(home+"/pyfi.ini")
            self.backend = CONFIG.get('backend', 'uri')
            self.broker = CONFIG.get('broker', 'uri')

        if celeryconfig is not None:
            import importlib

            module = importlib.import_module(celeryconfig.split['.'][:-1])
            celeryconfig = getattr(module, celeryconfig.split['.'][-1:])
            self.celery = Celery(include=self.processor.module)
            self.celery.config_from_object(celeryconfig)

        else:
            self.celery = Celery(
                'pyfi', backend=backend, broker=broker)

        self.process = None
        logging.info("Starting worker with pool[{}] backend:{} broker:{}".format(
            pool, backend, broker))

    def start(self):
        """
        Docstring
        """
        global processes
        from multiprocessing import Process
        import os

        def worker_proc(app, _queue):
            """ Set up celery queues for self.celery """
            import builtins
            import importlib
            import sys
            import json
            import time

            from billiard.pool import Pool

            logging.info("Processor beat: %s", self.processor.beat)

            queues = []
            engine = create_engine(self.dburi)

            session = sessionmaker(bind=engine)()
            self.processor = session.query(
                ProcessorModel).filter_by(id=self.processor.id).first()

            sio = socketio.Client()

            @sio.on('task', namespace='/tasks')
            def tmessage(message):
                print("message: ", message)

            @sio.on('queue', namespace='/tasks')
            def message(data):
                logging.info(
                    '\x1b[33;21m I received a message! %s\x1b[0m', data)

            @sio.on('connect', namespace='/tasks')
            def connect():
                logging.info("I'm connected to namespace /tasks!")

                sio.emit('servermsg', {
                    'module': self.processor.module }, namespace='/tasks')

                sio.emit('join', {'room': 'pyfi.queue1.proc1'}, namespace='/tasks')

            logging.info("Attempting connect to events server {}".format(events_server))
            while True:
                try:
                    sio.connect('http://'+events_server+':5000',
                                namespaces=['/tasks'])
                    logging.info(
                        "Connected to events server {}".format(events_server))
                    break
                except Exception as ex:
                    pass # Silent error

            if self.processor and self.processor.sockets and len(self.processor.sockets) > 0:
                for socket in self.processor.sockets:
                    logging.info("Socket %s",socket)
                    if socket.queue:
                        # TODO: Use socket.task.name as the task name and self.processor.module as the module
                        # For each socket task, use a queue named socket.queue.name+self.processor.name+socket.task.name
                        # for example: queue1.proc1.some_task_A, queue1.proc1.some_task_B

                        # This queue is bound to a broadcast(fanout) exchange that delivers
                        # a message to all the connected queues however sending a task to
                        # this queue will deliver to this processor only
                        processor_path = socket.queue.name + '.' + self.processor.name.replace(' ', '.')
                        if processor_path not in queues:
                            queues += [processor_path]
                            room = {'room': processor_path}
                            logging.info("Joining room %s", room)
                            sio.emit('join', room, namespace='/tasks')

                        processor_task = socket.queue.name + '.' + self.processor.name.replace(
                            ' ', '.')+'.'+socket.task.name
                        if processor_task not in queues:

                            room = {'room': processor_task}
                            queues += [processor_task]

                        # This topic queue represents the broadcast fanout to all workers connected
                        # to it. Sending a task to this queue delivers to all connected workers
                        queues += [socket.queue.name+'.topic']
                        from kombu import Exchange, Queue, binding
                        from kombu.common import Broadcast
                        logging.debug('socket.queue.expires %s', socket.queue.expires)
                        app.conf.task_queues = (
                            Broadcast(socket.queue.name+'.topic', queue_arguments={
                                'x-message-ttl': socket.queue.expires,
                                'x-expires': socket.queue.expires
                            }),
                            KQueue(
                                socket.queue.name+'.' +
                                self.processor.name.replace(
                                    ' ', '.')+'.'+socket.task.name,
                                #Exchange(socket.queue.name +
                                #         '.topic', type='fanout'),
                                Exchange(socket.queue.name + '.' + self.processor.name.replace(
                                    ' ', '.')+'.'+socket.task.name, type='direct'),
                                routing_key=socket.queue.name + '.' + self.processor.name.replace(
                                    ' ', '.')+'.'+socket.task.name,
                                message_ttl=socket.queue.message_ttl,
                                durable=socket.queue.durable,
                                expires=socket.queue.expires
                            ),
                            KQueue(
                                socket.queue.name+'.' +
                                self.processor.name.replace(
                                    ' ', '.'),
                                Exchange(socket.queue.name +
                                         '.topic', type='fanout'),
                                routing_key=socket.queue.name+'.' +
                                self.processor.name.replace(
                                    ' ', '.'),
                                message_ttl=socket.queue.message_ttl,
                                durable=socket.queue.durable,
                                expires=socket.queue.expires
                            ))

                        app.conf.task_routes = {
                            self.processor.module+'.'+socket.task.name: {
                                'queue': [socket.queue.name+'.topic', socket.queue.name],
                                'exchange': [socket.queue.name+'.topic', socket.queue.name]
                            }
                        }

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

            worker = app.Worker(
                hostname=self.processor.name+'@'+self.worker.hostname,
                backend=self.backend,
                broker=self.broker,
                beat=self.processor.beat,
                queues=queues,
                without_mingle=True,
                without_gossip=True,
                concurrency=int(self.processor.concurrency)
            )

            if self.processor.beat:
                worker.app.conf.beat_schedule = {
                    "run-me-every-ten-seconds": {
                        "task": "pyfi.harness",
                        "args": (self.processor.module, self.processor.task),
                        "schedule": self.processor.schedule
                    }
                }

            sys.path.append(os.getcwd())

            setattr(builtins, 'worker', worker)

            module = importlib.import_module(self.processor.module)
            _plugs = {}
            for plug in self.processor.plugs:
                _plugs[plug.queue.name] = []

            
            if self.processor and self.processor.sockets and len(self.processor.sockets) > 0:
                for socket in self.processor.sockets:
                    func = getattr(module, socket.task.name)

                    func = self.celery.task(func, name=self.processor.module +
                                            '.'+socket.task.name, retries=self.processor.retries)
                    
                    @task_prerun.connect(sender=func)
                    def pyfi_task_prerun(sender=None, **kwargs):
                        task_kwargs = kwargs.get('kwargs')
                        task_kwargs['plugs'] = _plugs
                        task_kwargs['output'] = {}

                    @task_success.connect(sender=func)
                    def pyfi_task_success(sender=None, **kwargs):
                        pass

                    @task_failure.connect(sender=func)
                    def pyfi_task_failure(sender=None, **kwargs):
                        pass

                    @task_internal_error.connect(sender=func)
                    def pyfi_task_internal_error(sender=None, **kwargs):
                        pass

                    @task_received.connect(sender=func)
                    def pyfi_task_received(sender=None, **kwargs):
                        pass

                    @task_postrun.connect(sender=func)
                    def pyfi_task_postrun(sender=None, **kwargs):
                        task_kwargs = kwargs.get('kwargs')
                        plugs = task_kwargs['plugs']

                        try:
                            while _queue.qsize() > 1000:
                                logging.info("Waiting for queue to shrink")
                                time.sleep(0.5)

                            data = {
                                'module': self.processor.module, 'message': 'Processor message', 'task': sender.__name__}

                            for socket in self.processor.sockets:
                                if socket.task.name == sender.__name__:
                                    processor_path = socket.queue.name + '.' + \
                                        self.processor.name.replace(' ', '.')
                                    data = {
                                        'module': self.processor.module, 'message': 'Processor message', 'channel': 'task', 'room': processor_path, 'task': sender.__name__}
                                    payload = json.dumps(data)
                                    data['message'] = payload
                                    break

                            logging.debug(data)

                            result = kwargs.get('args')[0]
                            data['message'] = json.dumps(result)
                            data['message'] = json.dumps(data)
                            logging.info(
                                "EMITTING ROOMSG: %s", data)
                            _queue.put(['servermsg', data])
                            _queue.put(['roomsg', data])

                            _queue.put(
                                ['roomsg', {'channel': 'log', 'room': processor_path, 'message': 'A log message!'}])

                            logging.debug("PLUGS: %s", plugs)
                            for key in plugs:

                                processor_plug = None

                                for _plug in self.processor.plugs:
                                    if _plug.queue.name == key:
                                        processor_plug = _plug

                                if processor_plug is None:
                                    continue

                                processors = self.database.session.query(
                                    ProcessorModel).filter(ProcessorModel.sockets.any(SocketModel.queue.has(name=key)))

                                for msg in plugs[key]:
                                    logging.info(
                                        "Sending {} to queue {}".format(msg, key))

                                    if processor_plug.queue.qtype == 'direct':
                                        for processor in processors:
                                            logging.debug("Invoking {}=>{}.{}({})".format(
                                                key, processor.module, processor.task, msg))

                                            # Target specific worker queue here
                                            worker_queue = key+'.' + \
                                                processor.name.replace(' ', '.')
                                            self.celery.signature(
                                                processor.module+'.'+processor.task, args=(msg,), queue=worker_queue, kwargs={}).delay()
                        except:
                            import traceback
                            print(traceback.format_exc())
                            pass

            worker.start()

        logging.info("Preparing worker %s %s %s %s %s", self.worker.name,
                     self.processor.plugs, self.backend, self.broker, self.worker.processor.module)

        os.chdir(self.workdir)
        import time

        if self.processor.gitrepo:
            logging.info("git clone -b {} --single-branch {} git".format(
                self.processor.branch, self.processor.gitrepo))
            shutil.rmtree("git", ignore_errors=True)

            while True:
                try:
                    os.system(
                        "git clone -b {} --single-branch {} git".format(self.processor.branch, self.processor.gitrepo))
                    sys.path.append(self.workdir+'/git')
                    os.chdir('git')
                    break
                except Exception as ex:
                    logging.error(ex)
                    time.sleep(3)

        process = Process(target=worker_proc, args=(self.celery, queue))
        processes += [process]
        process.start()
        logging.debug("PROCESS PID", process.pid)
        self.process = process

        def emit_messages():
            import json

            sio = socketio.Client()

            logging.info(
                "Attempting connect to events server {}".format(events_server))
            while True:
                try:
                    sio.connect('http://'+events_server+':5000',
                                namespaces=['/tasks'])
                    logging.info("Connected to events server {}".format(events_server))
                    break
                except Exception as ex:
                    pass  # Silent error

            last_qsize = 0
            while True:
                try:
                    message = queue.get()
                    sio.emit(*message, namespace='/tasks')
                except Exception as ex:
                    logging.error(ex)
                    time.sleep(3)

        process2 = Process(target=emit_messages)
        process2.daemon = True
        #print("PROCESS2 PID", process2.pid)
        #processes += [process2]
        process2.start()

        logging.info("Started worker process with pid[%s]", process.pid)
        return process

    def busy(self):
        """
        Docstring
        """
        #cinspect = celery.current_app.control.inspect()
        # cinspect.active()) + ccount(cinspect.scheduled()) + ccount(cinspect.reserved())
        pass

    def suspend(self):
        """
        Docstring
        """
        p = psutil.Process(self.process.pid)
        p.suspend()

    def resume(self):
        """
        Docstring
        """
        p = psutil.Process(self.process.pid)
        p.resume()

    def kill(self):
        """
        Docstring
        """
        logging.info("Terminating process")
        self.process.terminate()
        logging.info("Finishing.")
        self.process.join()
        if os.path.exists(self.workdir):
            logging.debug("Removing working directory %s", self.workdir)
            shutil.rmtree(self.workdir)
        logging.info("Done.")
