"""
Agent worker class. Primary task/code execution context for processors
"""
from datetime import timedelta
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
from celery.signals import worker_process_init


class Worker:
    """
    A worker is a celery worker with a processor module loaded and represents a single processor
    """

    def __init__(self, processor, workdir, database=None, backend='redis://192.168.1.23', config=None, broker='pyamqp://192.168.1.23'):
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

        if config is not None:
            import importlib

            module = importlib.import_module(config.split['.'][:-1])
            config = getattr(module, config.split['.'][-1:])
            self.celery = Celery()
            self.celery.config_from_object(config)
        else:
            self.celery = celery = Celery('pyfi', backend=backend, broker=broker)
        self.process = None
        logging.info("Starting worker {} {}".format(backend, broker))


    def start(self):
        """
        Docstring
        """
        from multiprocessing import Process
        import os

        def worker_proc(app):
            """ Set up celery queues for self.celery """

            logging.info("Processor beat: %s", self.processor.beat)
            # Expects that the gitrepo pull and commit provide
            # code at the module located by self.processor.module

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

            print("QUEUES:",queues)
            
            @worker_process_init.connect()
            def prep_db_pool(**kwargs):
                """
                    When Celery fork's the parent process, the db engine & connection pool is included in that.
                    But, the db connections should not be shared across processes, so we tell the engine
                    to dispose of all existing connections, which will cause new ones to be opend in the child
                    processes as needed.
                    More info: https://docs.sqlalchemy.org/en/latest/core/pooling.html#using-connection-pools-with-multiprocessing
                """
                # The "with" here is for a flask app using Flask-SQLAlchemy.  If you don't
                # have a flask app, just remove the "with" here and call .dispose()
                # on your SQLAlchemy db engine.
                print("Disposing engine")
                #self.database.dispose()

            worker = self.celery.Worker(
                include=self.processor.module,
                hostname=self.processor.name+'@'+self.worker.hostname,
                backend=self.backend,
                broker=self.broker,
                beat=self.processor.beat,
                queues=queues,
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

            import importlib

            module = importlib.import_module(self.processor.module)
            func = getattr(module, self.processor.task)


            @worker.app.task(name=self.processor.module+'.'+self.processor.task)
            def harness(message):
                plugs = {}
                for plug in self.processor.plugs:
                    plugs[plug.queue.name] = []

                result = func(message, plugs=plugs)
                for key in plugs:
                    for msg in plugs[key]:
                            print("Sending {} to queue {}".format(msg, key))
                            processors = self.database.session.query(
                                ProcessorModel).filter(ProcessorModel.outlets.any(OutletModel.queue.has(name=key)))
                            print("Linked Processors: ", [
                                  processor.name for processor in processors])
                            # Use workerpool to invoke
                            # Query all processors with outlets connected to this queue
                            # Obtain their module and tasks, construct harness call
                            # Invoke

                            for processor in processors:
                                print("Invoking {}=>{}.{}({})".format(key, processor.module,processor.task, result))

                                proc = Processor(key, processor.module+'.'+processor.task)
                                proc(result)

                return result
            
            worker.start()

        logging.info("Starting worker %s %s %s %s %s", self.worker.name,
                     self.processor.plugs, self.backend, self.broker, self.worker.processor.module)

        # Pull git commit into workdir
        # self.processor.gitrepo, self.processor.commit
        # If no module code located at self.processor.module then put an error on the processor
        os.chdir(self.workdir)
        print(self.workdir)
        if self.processor.gitrepo:
            print(os.getcwd())
            logging.info("git clone -b {} --single-branch {} git".format(
                self.processor.branch, self.processor.gitrepo))
            shutil.rmtree("git", ignore_errors=True)
            os.system(
                "git clone -b {} --single-branch {} git".format(self.processor.branch, self.processor.gitrepo))
            sys.path.append(self.workdir+'/git')
            print(os.getcwd())
            os.chdir('git')

        process = Process(target=worker_proc, daemon=True, args=(self.celery,))
        process.start()
        self.process = process

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
