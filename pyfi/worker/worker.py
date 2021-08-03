"""
Agent workerclass. Primary task/code execution context for processors
"""
import logging
import shutil
import os
import sys
import psutil

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyfi.db.model import UserModel, AgentModel, WorkerModel, PlugModel, OutletModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel
from pyfi.processor import Processor

from celery import Celery
from celery.signals import worker_process_init, after_task_publish, task_success, task_prerun, task_postrun, task_failure, task_internal_error, task_received


class Worker:
    """
    A worker is a celery worker with a processor module loaded and represents a single processor
    """

    def __init__(self, processor, workdir, pool=4, database=None, backend='redis://192.168.1.23', config=None, broker='pyamqp://192.168.1.23'):
        """
        """
        from pyfi.db.model import Base

        self.processor = processor
        self.worker = processor.worker
        self.backend = backend
        self.broker = broker
        self.workdir = workdir
        self.database = database
        self.dburi = database.uri
        self.pool = pool

        if config is not None:
            import importlib

            module = importlib.import_module(config.split['.'][:-1])
            config = getattr(module, config.split['.'][-1:])
            self.celery = Celery(include=self.processor.module)
            self.celery.config_from_object(config)
        else:
            self.celery = celery = Celery(
                'pyfi', backend=backend, broker=broker)
        self.process = None
        logging.info("Starting worker with pool[{}] backend:{} broker:{}".format(pool, backend, broker))


    def start(self):
        """
        Docstring
        """
        from multiprocessing import Process
        import os

        def worker_proc(app):
            """ Set up celery queues for self.celery """
            import builtins
            import importlib
            import sys
            from billiard.pool import Pool
            
            logging.info("Processor beat: %s", self.processor.beat)

            queues = []
            engine = create_engine(self.dburi)

            session = sessionmaker(bind=engine)()
            self.processor = session.query(
                ProcessorModel).filter_by(id=self.processor.id).first()
                
            if self.processor and self.processor.outlets and len(self.processor.outlets) > 0:
                for outlet in self.processor.outlets:
                    if outlet.queue:
                        print("queue: ",outlet.queue)
                        queues += [outlet.queue.name]

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

            setattr(builtins,'worker',worker)

            module = importlib.import_module(self.processor.module)
            func = getattr(module, self.processor.task)

            _plugs = {}
            for plug in self.processor.plugs:
                _plugs[plug.queue.name] = []

            # Processor properties are set on the task here
            func = self.celery.task(func, name=self.processor.module+'.'+self.processor.task, retries=self.processor.retries)

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
                for key in plugs:
                    for msg in plugs[key]:
                        logging.info("Sending {} to queue {}".format(msg, key))

                        processors = self.database.session.query(
                            ProcessorModel).filter(ProcessorModel.outlets.any(OutletModel.queue.has(name=key)))

                        for processor in processors:
                            print("Invoking {}=>{}.{}({})".format(
                                key, processor.module, processor.task, msg))
                            self.celery.signature(
                                processor.module+'.'+processor.task, args=(msg,), queue=key, kwargs={}).delay()
            
            worker.start()

        logging.info("Preparing worker %s %s %s %s %s", self.worker.name,
                     self.processor.plugs, self.backend, self.broker, self.worker.processor.module)

        os.chdir(self.workdir)
        
        if self.processor.gitrepo:
            logging.info("git clone -b {} --single-branch {} git".format(
                self.processor.branch, self.processor.gitrepo))
            shutil.rmtree("git", ignore_errors=True)
            os.system(
                "git clone -b {} --single-branch {} git".format(self.processor.branch, self.processor.gitrepo))
            sys.path.append(self.workdir+'/git')
            os.chdir('git')

        process = Process(target=worker_proc, args=(self.celery,))
        process.start()
        self.process = process
        logging.info("Started worker process with pid[%s]", process.pid)
        return process

    def busy(self):
        """
        Docstring
        """
        #cinspect = celery.current_app.control.inspect()
        #cinspect.active()) + ccount(cinspect.scheduled()) + ccount(cinspect.reserved())
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
