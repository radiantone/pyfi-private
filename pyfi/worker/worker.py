"""
Agent workerclass. Primary task/code execution context for processors
"""
from kombu import serialization
from pyfi.db.model.models import use_identity
import redis
import logging
import shutil
import os
import sys
import psutil
import signal
import configparser
import platform
from functools import partial
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from pathlib import Path
from multiprocessing import Condition, Queue

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyfi.db.model import UserModel, AgentModel, WorkerModel, PlugModel, SocketModel, JobModel, CallModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel

from celery import Celery
from celery.signals import setup_logging
from celery.signals import worker_process_init, after_task_publish, task_success, task_prerun, task_postrun, task_failure, task_internal_error, task_received
from kombu import Exchange, Queue as KQueue



@setup_logging.connect
def setup_celery_logging(**kwargs):
    logging.debug("DISABLE LOGGING SETUP")
    pass

home = str(Path.home())
CONFIG = configparser.ConfigParser()

events_server = os.environ['EVENTS'] if 'EVENTS' in os.environ else 'localhost'
lock = Condition()
queue = Queue()

hostname = platform.node()

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

def dispatcher(task):
    print("DISPATCHER",task)

def myfunc():
    print("my func triggered")


class Worker:
    """
    A worker is a celery worker with a processor module loaded and represents a single processor
    """
    from contextlib import contextmanager

    @contextmanager
    def get_session(self):
        session = self.database.session

        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            try:
                session.commit()
            except:
                session.rollback()


    def __init__(self, processor, workdir, pool=4, database=None, user=None, usecontainer=False, skipvenv=False, backend='redis://localhost', celeryconfig=None, broker='pyamqp://localhost'):
        """
        """
        from pyfi.db.model import Base

        self.processor = processor
        self.worker = processor.worker
        self.backend = backend
        self.broker = broker
        self.workdir = workdir
        self.dburi = database
        self.skipvenv = skipvenv
        self.usecontainer = usecontainer
        self.database = create_engine(self.dburi, pool_size=5, max_overflow=0)
        self.session = sessionmaker(bind=self.database)()
        self.database.session = self.session
        self.pool = pool
        self.user = user

        logging.debug("New Worker init: %s", processor)

        if os.path.exists(home+"/pyfi.ini"):
            CONFIG.read(home+"/pyfi.ini")
            self.backend = CONFIG.get('backend', 'uri')
            self.broker = CONFIG.get('broker', 'uri')

            jobstores = {
                'default': SQLAlchemyJobStore(url=CONFIG.get('database', 'uri'), tablename='jobs')
            }
            executors = {
                'default': ThreadPoolExecutor(20),
                'processpool': ProcessPoolExecutor(5)
            }
            job_defaults = {
                'coalesce': False,
                'max_instances': 3
            }

            self.scheduler = BackgroundScheduler(jobstores=jobstores, executors = executors, job_defaults = job_defaults, timezone = utc)

            jobs = self.database.session.query(
                JobModel).all()

            self.jobs = {}

            for job in jobs:
                self.jobs[job.id] = job

            logging.debug("JOBS %s",self.jobs)

            self.scheduler.start()
            self.scheduler.print_jobs()


        if celeryconfig is not None:
            logging.info("Applying celeryconfig from %s", celeryconfig)
            import importlib

            module = importlib.import_module(celeryconfig.split['.'][:-1])
            celeryconfig = getattr(module, celeryconfig.split['.'][-1:])
            self.celery = Celery(include=self.processor.module)
            self.celery.config_from_object(celeryconfig)

        else:
            self.celery = Celery(
                'pyfi', backend=backend, broker=broker)

            from pyfi.celery import config
            logging.info("App config is %s", config)
            self.celery.config_from_object(config)

        self.process = None
        logging.debug("Starting worker with pool[{}] backend:{} broker:{}".format(
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

        if not self.usecontainer:
            cmd = ["venv/bin/pyfi", "worker", "start", "-s",
                   "-n", name]
            if self.user:
                #cmd = ["runuser", "-u", self.user, "--", "venv/bin/pyfi", "worker", "start", "-s",
                #       "-n", name]
                cmd = ["venv/bin/pyfi", "worker", "start", "-s",
                       "-n", name]

            logging.info("Launching worker %s %s", cmd, name)
            self.process = process = Popen(cmd, stdout=sys.stdout, stderr=sys.stdout, preexec_fn=os.setsid)

            logging.debug("Worker launched successfully: process %s.",
                        self.process.pid)
        else:
            """ Run agent worker inside previously launched container """
            pass

        return process

    def start(self, start=True, listen=True):
        """
        Docstring
        """
        global processes
        from multiprocessing import Process
        import os

        logging.debug("PYTHON: %s", sys.executable)

        def worker_proc(app, _queue):
            """ Set up celery queues for self.celery """
            import builtins
            import importlib
            import sys
            import json
            import time

            from billiard.pool import Pool

            queues = []
            engine = create_engine(self.dburi)

            session = sessionmaker(bind=engine)()
            self.processor = session.query(
                ProcessorModel).filter_by(id=self.processor.id).first()

            task_queues = []
            task_routes = {}

            if self.processor and self.processor.sockets and len(self.processor.sockets) > 0:
                logging.info("Setting up sockets...")
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

                        logging.info("Joining room %s", processor_path)
                        if processor_path not in queues:
                            queues += [processor_path]

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
                                    'x-expires': 300}
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
                                    'x-expires': 300}
                            )
                        ]

                        task_routes[self.processor.module+'.'+socket.task.name] = {
                            'queue': socket.queue.name,
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

            logging.info("Starting celery worker %s %s %s",
                         self.processor.name+'@'+hostname, self.backend, self.broker)

            worker = app.Worker(
                hostname=self.processor.name+'@'+hostname,
                backend=self.backend,
                broker=self.broker,
                beat=self.processor.beat,
                uid='darren',
                without_mingle=True,
                without_gossip=True,
                concurrency=int(self.processor.concurrency)
            )
            self.processor.worker.hostname = hostname

            # Find existing model first
            try:
                workerModel = self.database. session.query(
                    WorkerModel).filter_by(name=hostname+".agent."+self.processor.name+'.worker').first()

                if workerModel is None:
                    workerModel = WorkerModel(name=hostname+".agent."+self.processor.name+'.worker', concurrency=int(self.processor.concurrency),
                                              status='ready',
                                              backend=self.backend,
                                              broker=self.broker,
                                              hostname=hostname,
                                              requested_status='start')

                    with self.get_session() as session:
                        session.add(workerModel)

            except:
                pass

            if self.processor.beat:
                worker.app.conf.beat_schedule = {}

                for socket in self.processor.sockets:
                    if socket.interval <= 0:
                        continue
                    tkey = socket.queue.name+'.' + self.processor.name.replace(
                        ' ', '.')+'.'+socket.task.name
                    
                    worker_queue = KQueue(
                        tkey,
                        Exchange(socket.queue.name, type='direct'),
                        routing_key=tkey,

                        message_ttl=socket.queue.message_ttl,
                        durable=socket.queue.durable,
                        expires=socket.queue.expires,
                        queue_arguments={
                            'x-message-ttl': 30000,
                            'x-expires': 300}
                    )

                    worker.app.conf.beat_schedule[self.processor.module+'.'+socket.task.name] = {
                        "task": self.processor.module+'.'+socket.task.name,
                        "args": ("Hello World!",),
                        "schedule": socket.interval,
                        'options': {'queue': tkey},
                    }

            sys.path.append(os.getcwd())

            setattr(builtins, 'worker', worker)

            logging.debug("CWD %s", os.getcwd())

            module = importlib.import_module(self.processor.module)

            _plugs = {}

            for plug in self.processor.plugs:
                _plugs[plug.queue.name] = []

            if self.processor and self.processor.sockets and len(self.processor.sockets) > 0:
                for socket in self.processor.sockets:
                                        
                    if socket.scheduled:
                        try:
                            if socket.schedule_type == 'CRON':
                                print("ADDING CRON JOB TYPE")

                            elif socket.schedule_type == 'INTERVAL':
                                if socket.name not in self.jobs:
                                    self.scheduler.add_job(dispatcher, 'interval', args=[
                                        socket.task], jobstore='default', misfire_grace_time=60, coalesce=True, max_instances=1, seconds=socket.intveral, id=socket.name)
                                    logging.info("Scheduled socket %s",socket.name)
                        except:
                            logging.info("Already scheduled this socket %s",socket.name)
                    
                    func = getattr(module, socket.task.name)

                    func = self.celery.task(func, name=self.processor.module +
                                            '.'+socket.task.name, retries=self.processor.retries)

                    @task_prerun.connect()
                    def pyfi_task_prerun(sender=None, task_id=None, **kwargs):
                        from datetime import datetime
                        from uuid import uuid4

                        # Store task run data
                        task_kwargs = kwargs.get('kwargs')
                        task_kwargs['plugs'] = _plugs
                        task_kwargs['output'] = {}

                        logging.info("KWARGS BEFORE: %s", task_kwargs)
                        if 'tracking' not in task_kwargs:
                            task_kwargs['tracking'] = str(uuid4())

                        logging.info("KWARGS: %s",task_kwargs)
                        for _socket in self.processor.sockets:
                            if _socket.task.name == sender.__name__:
                                processor_path = _socket.queue.name + '.' + \
                                    self.processor.name.replace(' ', '.')
                                started = datetime.now()
                                data = ['roomsg', {'channel': 'task', 'state': 'running', 'date': str(started), 'room': processor_path}]
                                logging.info("Task PRERUN: %s %s", sender, data)
                                _queue.put(data)
                                call = CallModel(
                                    name=self.processor.module+'.'+_socket.task.name, resultid='celery-task-meta-'+task_id, celeryid=task_id, task_id=_socket.task.id, state='running', started=started)
                                
                                with self.get_session() as session:
                                    session.add(call)

                                logging.info("COMMITTED CALL ID %s",task_id)

                                
                    @task_success.connect()
                    def pyfi_task_success(sender=None, **kwargs):
                        logging.info("Task SUCCESS: %s", sender)
                        # Store task run data
                        pass

                    @task_failure.connect()
                    def pyfi_task_failure(sender=None, **kwargs):
                        # Store task run data
                        pass

                    @task_internal_error.connect()
                    def pyfi_task_internal_error(sender=None, **kwargs):
                        # Store task run data
                        pass

                    @task_received.connect()
                    def pyfi_task_received(sender=None, **kwargs):
                        logging.info("Task RECEIVED %s", sender)
                        pass

                    @task_postrun.connect()
                    def pyfi_task_postrun(sender=None, task_id=None, retval=None, **kwargs):
                        from datetime import datetime

                        logging.info("Task POSTRUN [%s] %s KWARGS: %s", task_id, sender, kwargs)

                        logging.info("Task POSTRUN RESULT %s", retval)

                        session = self.database.session

                        task_kwargs = kwargs.get('kwargs')
                        plugs = task_kwargs['plugs']

                        pass_kwargs = {}

                        if 'tracking' in kwargs:
                            pass_kwargs['tracking'] = kwargs['kwargs']['tracking']

                        try:
                            call = session.query(
                                CallModel).filter_by(celeryid=task_id).first()

                            if call:
                                call.finished = datetime.now()
                                call.state = 'finished'
                                try:
                                    session.add(call)
                                    session.commit()
                                except:
                                    session.rollback()
                        except:
                            logging.error("No pre-existing Call object for task %s", task_id)
                        try:
                            # while _queue.qsize() > 1000:
                            #    logging.debug("Waiting for queue to shrink")
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
                                        'module': self.processor.module, 'date': str(datetime.now()), 'resultkey': 'celery-task-meta-'+task_id, 'message': 'Processor message', 'channel': 'task', 'room': processor_path, 'task': sender.__name__}
                                    payload = json.dumps(data)
                                    data['message'] = payload
                                    break

                            logging.info(data)

                            result = kwargs.get('args')[0]
                            data['message'] = json.dumps(result)
                            data['message'] = json.dumps(data)
                            data['state'] = 'postrun'

                            logging.debug(
                                "EMITTING ROOMSG: %s", data)

                            #_queue.put(['servermsg', data])
                            _queue.put(['roomsg', data])

                            _queue.put(
                                ['roomsg', {'channel': 'log', 'date': str(datetime.now()), 'room': processor_path, 'message': 'A log message!'}])

                            logging.debug("PLUGS: %s", plugs)
                            for key in plugs:
                                """
                                Find plugs on this processor whose queue matches key
                                and then invoke the task for plug.socket.task
                                """
                                processor_plug = None

                                for _plug in self.processor.plugs:
                                    if _plug.queue.name == key:
                                        processor_plug = _plug

                                if processor_plug is None:
                                    continue

                                logging.info("processor_plug %s",
                                             processor_plug)
                                # Get all processors where processor_plug is plugged into a socket
                                processors = self.database.session.query(
                                    ProcessorModel).filter(ProcessorModel.sockets.any(SocketModel.queue.has(name=key)))

                                processor_map = {}
                                for p in processors:
                                    processor_map[str(p.id)] = p

                                msgs = [msg for msg in plugs[key]]
                                logging.info("msgs %s", msgs)

                                for msg in msgs:
                                    """ We have data in an outbound queue and need to find the associated plug and socket to construct the call"""
                                    logging.debug(
                                        "Sending {} to queue {}".format(msg, key))

                                    if processor_plug.queue.qtype == 'direct':
                                        logging.info("Finding processor....")
                                        for socket in processor_plug.sockets:
                                            logging.info(
                                                "Checking socket[%s] vs key[%s]", socket.queue.name, key)
                                            _processor = processor_map[socket.processor_id]
                                            if socket.queue.name == key:
                                                """ Find the socket object for the outbound queue"""
                                                logging.info("Invoking {}=>{}({})".format(
                                                    key,
                                                    _processor.module+'.'+socket.task.name, msg))

                                                tkey = key+'.' + _processor.name.replace(
                                                    ' ', '.')+'.'+socket.task.name
                                                # Target specific worker queue here
                                                worker_queue = KQueue(
                                                    tkey,
                                                    Exchange(
                                                        key, type='direct'),
                                                    routing_key=tkey,

                                                    message_ttl=socket.queue.message_ttl,
                                                    durable=socket.queue.durable,
                                                    expires=socket.queue.expires,
                                                    # expires=30,
                                                    # socket.queue.message_ttl
                                                    # socket.queue.expires
                                                    queue_arguments={
                                                        'x-message-ttl': 30000,
                                                        'x-expires': 300}
                                                )

                                                logging.info(
                                                    "worker queue %s", worker_queue)
                                                try:
                                                    # TODO: Add kwarg injected objects for redis, _queue for pubsub, processor object or json, metadata
                                                    # Define context object that function can use to set outbound data and get inbound data
                                                    # Avoid risky direct object access in favor of context hashmap that is used by framework prerun/postrun
                                                    logging.info("PASS_KWARGS: %s",pass_kwargs)
                                                    self.celery.signature(
                                                        _processor.module+'.'+socket.task.name, args=(msg,), queue=worker_queue, kwargs=pass_kwargs).delay()
                                                except:
                                                    import traceback
                                                    print(
                                                        traceback.format_exc())
                                                logging.info(
                                                    "call complete %s %s %s", _processor.module+'.'+socket.task.name, (msg,), worker_queue)
                                            # We sent the message, so remove it so it doesn't get re-sent on the next cycle
                                            # If there is an exception delivering the message above, this code will get skipped and the
                                            # cycle will retry this message
                                            plugs[key].remove(msg)

                        except:
                            import traceback
                            logging.debug(traceback.format_exc())
                            pass

            worker.start()

        logging.debug("Preparing worker %s %s %s %s %s", self.worker.name,
                      self.processor.plugs, self.backend, self.broker, self.worker.processor.module)

        os.chdir(self.workdir)
        import time

        if self.processor.gitrepo and not self.skipvenv:


            if self.usecontainer:
                """ Launch pyfi:latest container passing in variables and gitrepo. Maintain reference to launched container"""

            else:
                """ Build our virtualenv and import the gitrepo for the processor """
                logging.debug("git clone -b {} --single-branch {} git".format(
                    self.processor.branch, self.processor.gitrepo))

                if os.path.exists("git"):
                    os.chdir('git')
                    logging.info("Pulling update from git")
                    os.system('git config --get remote.origin.url')
                    os.system('git config pull.rebase false')
                    os.system('git pull')
                else:

                    while True:
                        try:
                            logging.info("git clone -b {} --single-branch {} git".format(
                                self.processor.branch, self.processor.gitrepo.split('#')[0]))
                            os.system(
                                "git clone -b {} --single-branch {} git".format(self.processor.branch, self.processor.gitrepo.split('#')[0]))
                            sys.path.append(self.workdir+'/git')
                            os.chdir('git')
                            os.system("git config credential.helper store")
                            break
                        except Exception as ex:
                            logging.error(ex)
                            time.sleep(3)

                if not os.path.exists('venv'):
                    from virtualenvapi.manage import VirtualEnvironment

                    logging.info("Building virtualenv...in %s", os.getcwd())

                    env = VirtualEnvironment(
                        'venv', python=sys.executable, system_site_packages=True)  # inside git directory

                    login = os.environ['GIT_LOGIN']
                    env.install('-e git+'+login +
                                '/radiantone/pyfi-private#egg=pyfi')

                    try:
                        env.install('-e git+'+self.processor.gitrepo.strip())
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

            redisclient = redis.Redis.from_url(self.backend)

            last_qsize = 0
            while True:
                try:
                    message = queue.get()
                    logging.info("Emitting message %s %s", message[1]['room'], message)
                    redisclient.publish(message[1]['room']+'.'+message[1]['channel'],json.dumps(message[1]))
                    #sio.emit(*message, namespace='/tasks')
                except Exception as ex:
                    logging.error(ex)
                    time.sleep(3)

        process2 = Process(target=emit_messages)
        process2.daemon = True

        # if listen:
        logging.info("Starting emit_messages")
        process2.start()

        logging.debug("Started worker process with pid[%s]", process.pid)
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
        logging.debug("Terminating process %s", self.process.pid)

        process = psutil.Process(self.process.pid)

        for child in process.children(recursive=True):
            child.kill()
            
        process.kill()
        process.terminate()

        os.killpg(os.getpgid(process.pid), 15)
        os.kill(process.pid, signal.SIGKILL)

        logging.debug("Finishing.")

        try:
            self.process.join()
        except:
            pass

        if os.path.exists(self.workdir):
            logging.debug("Removing working directory %s", self.workdir)
            shutil.rmtree(self.workdir)

        logging.debug("Done killing worker.")
