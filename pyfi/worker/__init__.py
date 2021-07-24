import psutil
import os
import signal
import logging

from celery import Celery


class Worker:
    """
    A worker is a celery worker with a processor module loaded and represents a single processor
    """

    def __init__(self, worker, backend='redis://192.168.1.23', broker='pyamqp://192.168.1.23'):
        self.worker = worker
        self.backend = backend
        self.broker = broker
        self.celery = Celery('pyfi', backend=backend, broker=broker)

        @self.celery.task
        def shout():
            print("WORKER SHOUT!")

    def start(self):
        from multiprocessing import Process
        import time
        import psutil
        import os
        import signal

        def worker_proc():
            worker = self.celery.Worker(
                include=self.worker.processor.module,
                hostname=self.worker.name,
                backend=self.backend,
                broker=self.broker,
                queues=[queue.name for queue in self.worker.queues],
                concurrency=int(self.worker.concurrency)
            )
            worker.start()

        logging.info("Starting worker %s %s %s %s", self.worker.name,
                         self.worker.queues, self.backend, self.broker)
        process = Process(target=worker_proc)
        process.start()
        self.process = process

    def suspend(self):
        p = psutil.Process(self.process.pid)
        p.suspend()

    def resume(self):
        p = psutil.Process(self.process.pid)
        p.resume()

    def kill(self):
        #pgrp = os.getpgid(self.process.pid)

        #os.killpg(pgrp, signal.SIGKILL)
        self.process.terminate()
        self.process.join()
        #self.process.kill()


