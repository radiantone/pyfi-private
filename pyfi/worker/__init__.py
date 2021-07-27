"""
Agent worker class. Primary task/code execution context for processors
"""
import logging
import shutil
import os
import psutil

from celery import Celery


class Worker:
    """
    A worker is a celery worker with a processor module loaded and represents a single processor
    """

    def __init__(self, processor, workdir, backend='redis://192.168.1.23', broker='pyamqp://192.168.1.23'):
        """
        """
        self.processor = processor
        self.worker = processor.worker
        self.backend = backend
        self.broker = broker
        self.workdir = workdir
        self.celery = Celery('pyfi', backend=backend, broker=broker)

        @self.celery.task
        def shout():
            print("WORKER SHOUT!")

    def start(self):
        """
        Docstring
        """
        from multiprocessing import Process
        import os

        def worker_proc():
            queues = self.processor.queues
            for queue in queues:
                print(queue)
                """ Set up celery queues for self.celery """

            os.chdir(self.workdir)

            if self.processor.gitrepo:
                os.system('git clone '+self.processor.gitrepo+' git')
                os.chdir(self.workdir+'/git')

                if self.processor.commit:
                    os.system('git checkout '+self.processor.commit)
                    
            # Expects that the gitrepo pull and commit provide
            # code at the module located by self.processor.module
            worker = self.celery.Worker(
                include=self.processor.module,
                hostname=self.processor.name+'@'+self.worker.hostname,
                backend=self.backend,
                broker=self.broker,
                queues=[queue.name for queue in self.processor.queues],
                concurrency=int(self.processor.concurrency)
            )
            worker.start()

        logging.info("Starting worker %s %s %s %s %s", self.worker.name,
                     self.processor.queues, self.backend, self.broker, self.worker.processor.module)


        # Pull git commit into workdir
        # self.processor.gitrepo, self.processor.commit
        # If no module code located at self.processor.module then put an error on the processor

        process = Process(target=worker_proc)
        process.start()
        self.process = process

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
