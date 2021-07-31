from celery import Celery

class Processor:

    celery = Celery('pyfi', backend='redis://192.168.1.23',
                broker='pyamqp://192.168.1.23')

    def __init__(self, queue, name):
        self.name = name
        self.queue = queue

    def __call__(self, *args, **kwargs):

        # Add logging callbacks in here
        return self.celery.signature(self.name, args=args, queue=self.queue, kwargs=kwargs).delay()
