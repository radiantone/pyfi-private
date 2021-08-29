"""
Agent workerclass. Primary task/code execution context for processors
"""
import socketio
import logging
import shutil
import os
import sys
import psutil
import signal
import configparser
import platform

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

hostname = platform.node()


@setup_logging.connect
def setup_celery_logging(**kwargs):
    logging.debug("DISABLE LOGGING SETUP")
    pass


home = str(Path.home())
CONFIG = configparser.ConfigParser()

events_server = os.environ['EVENTS'] if 'EVENTS' in os.environ else 'localhost'
lock = Condition()
queue = Queue()

global processes
processes = []


def shutdown(*args):
    from psutil import Process

    for process in processes:
        try:
            process = Process(process.pid)
            for child in process.children(recursive=True):
                child.kill()
            process.kill()
            process.terminate()
            os.killpg(os.getpgid(process.pid), 15)
            os.kill(process.pid, signal.SIGKILL)
        except:
            pass

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
        logging.info("New Worker init: %s",processor)
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

    def launch(self, name):
        from subprocess import Popen
        from multiprocessing import Process

        """
        This method is used by the agent after the Worker() has been created and configured its venv.
        It is then launched using a subprocess running from that virtualenv
        The 'pyfi worker start' command will itself, run the start() method below.

        workerproc = Popen(["venv/bin/pyfi","worker","start","-n",processor['processor'].worker.name])
        """

        """
        import signal
        def start_worker():
            Popen(["venv/bin/pyfi", "worker", "start",
                   "-n", name], preexec_fn=os.setsid)
            print("Started worker", "venv/bin/pyfi", "worker", "start",
                  "-n", name)

        process = Process(target=start_worker)
        logging.info("Launching worker process...")
        process.start()
        self.process = process
        """
        logging.info("CWD: %s", os.getcwd())
        logging.info("Launching worker %s %s", "venv/bin/pyfi worker start -n %s", name)
        self.process = process = Popen(["venv/bin/pyfi", "worker", "start",
                         "-n", name], preexec_fn=os.setsid)

        logging.info("Worker launched successfully.")
        return process

    def start(self, start=True):
        """
        Docstring
        """
        global processes
        from multiprocessing import Process
        import os

        logging.info("PYTHON: %s",sys.executable)

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
                    'module': self.processor.module}, namespace='/tasks')

                sio.emit('join', {'room': 'pyfi.queue1.proc1'},
                         namespace='/tasks')

            logging.info(
                "Attempting connect to events server {}".format(events_server))
            while True:
                try:
                    sio.connect('http://'+events_server+':5000',
                                namespaces=['/tasks'])
                    logging.info(
                        "Connected to events server {}".format(events_server))
                    break
                except Exception as ex:
                    pass  # Silent error

            task_queues = []
            task_routes = {}

            if self.processor and self.processor.sockets and len(self.processor.sockets) > 0:
                for socket in self.processor.sockets:
                    logging.info("Socket %s", socket)
                    if socket.queue:

                        # TODO: Use socket.task.name as the task name and self.processor.module as the module
                        # For each socket task, use a queue named socket.queue.name+self.processor.name+socket.task.name
                        # for example: queue1.proc1.some_task_A, queue1.proc1.some_task_B

                        # This queue is bound to a broadcast(fanout) exchange that delivers
                        # a message to all the connected queues however sending a task to
                        # this queue will deliver to this processor only
                        processor_path = socket.queue.name + '.' + \
                            self.processor.name.replace(' ', '.')

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
                        queues += []
                        from kombu import Exchange, Queue, binding
                        from kombu.common import Broadcast
                        logging.debug('socket.queue.expires %s',
                                      socket.queue.expires)

                        task_queues += [
                            KQueue(
                                socket.queue.name+'.' +
                                self.processor.name.replace(
                                    ' ', '.')+'.'+socket.task.name,
                                Exchange(socket.queue.name + '.' + self.processor.name.replace(
                                    ' ', '.')+'.'+socket.task.name, type='direct'),
                                routing_key=socket.queue.name + '.' + self.processor.name.replace(
                                    ' ', '.')+'.'+socket.task.name,
                                message_ttl=socket.queue.message_ttl,
                                durable=socket.queue.durable,
                                expires=socket.queue.expires,
                                # socket.queue.message_ttl
                                # socket.queue.expires
                                queue_arguments={
                                    'x-message-ttl': 30000,
                                    'x-expires': 30}
                            )
                        ]

                        task_queues += [
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
                                expires=socket.queue.expires,
                                queue_arguments={
                                    'x-message-ttl': 30000,
                                    'x-expires': 30}
                            )
                        ]

                        task_routes[self.processor.module+'.'+socket.task.name] = {
                            'queue': [socket.queue.name],
                            'exchange': [socket.queue.name+'.topic', socket.queue.name]
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

            app.conf.task_queues = task_queues
            app.conf.task_routes = task_routes

            worker = app.Worker(
                hostname=self.processor.name+'@'+self.worker.hostname,
                backend=self.backend,
                broker=self.broker,
                beat=self.processor.beat,
                # queues=queues,
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
            print("CWD ", os.getcwd())
            module = importlib.import_module(self.processor.module)
            _plugs = {}
            for plug in self.processor.plugs:
                _plugs[plug.queue.name] = []

            if self.processor and self.processor.sockets and len(self.processor.sockets) > 0:
                for socket in self.processor.sockets:
                    func = getattr(module, socket.task.name)

                    func = self.celery.task(func, name=self.processor.module +
                                            '.'+socket.task.name, retries=self.processor.retries)

                    @task_prerun.connect()
                    def pyfi_task_prerun(sender=None, **kwargs):
                        logging.info("Task prerun")
                        task_kwargs = kwargs.get('kwargs')
                        task_kwargs['plugs'] = _plugs
                        task_kwargs['output'] = {}

                    @task_success.connect()
                    def pyfi_task_success(sender=None, **kwargs):
                        pass

                    @task_failure.connect()
                    def pyfi_task_failure(sender=None, **kwargs):
                        pass

                    @task_internal_error.connect()
                    def pyfi_task_internal_error(sender=None, **kwargs):
                        pass

                    @task_received.connect()
                    def pyfi_task_received(sender=None, **kwargs):
                        logging.info("Task received")
                        pass

                    @task_postrun.connect()
                    def pyfi_task_postrun(sender=None, **kwargs):
                        from datetime import datetime

                        print("pyfi_task_postrun")
                        task_kwargs = kwargs.get('kwargs')
                        plugs = task_kwargs['plugs']
                        try:
                            # while _queue.qsize() > 1000:
                            #    logging.info("Waiting for queue to shrink")
                            #    time.sleep(0.5)

                            # Create MetricDataModel and save to database
                            # time, size, processor, host, module, task, flow, owner
                            # Send this over 'data' channel

                            data = {
                                'module': self.processor.module, 'message': 'Processor message', 'task': sender.__name__}

                            for socket in self.processor.sockets:
                                if socket.task.name == sender.__name__:
                                    processor_path = socket.queue.name + '.' + \
                                        self.processor.name.replace(' ', '.')
                                    data = {
                                        'module': self.processor.module, 'date': str(datetime.now()), 'message': 'Processor message', 'channel': 'task', 'room': processor_path, 'task': sender.__name__}
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
                                ['roomsg', {'channel': 'log', 'date': str(datetime.now()), 'room': processor_path, 'message': 'A log message!'}])

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
                                                processor.name.replace(
                                                    ' ', '.')
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

            logging.info("Building virtualenv...in %s", os.getcwd())
            from virtualenvapi.manage import VirtualEnvironment
            env = VirtualEnvironment('venv', python=sys.executable, system_site_packages=True)  # inside git directory
            env.install('-e git+https://github.com/radiantone/pyfi-private#egg=pyfi')
            try:
                env.install('git+'+self.processor.gitrepo.strip())
            except:
                logging.error("Could not install %s",
                              self.processor.gitrepo.strip())
            
        process = Process(target=worker_proc, args=(self.celery, queue))
        process.app = self.celery
        processes += [process]

        if start:
            process.start()

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
                    logging.info(
                        "Connected to events server {}".format(events_server))
                    break
                except Exception as ex:
                    pass  # Silent error

            last_qsize = 0
            while True:
                try:
                    message = queue.get()
                    print("GOT MESSAGE FROM QUEUE",message)
                    sio.emit(*message, namespace='/tasks')
                except Exception as ex:
                    logging.error(ex)
                    time.sleep(3)

        process2 = Process(target=emit_messages)
        process2.daemon = True

        logging.info("Starting emit_messages")

        if start:
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
        os.kill(self.process.pid, signal.SIGKILL)
        self.process.terminate()
        logging.info("Finishing.")
        self.process.join()
        if os.path.exists(self.workdir):
            logging.debug("Removing working directory %s", self.workdir)
            shutil.rmtree(self.workdir)
        logging.info("Done.")
