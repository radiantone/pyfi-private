from celery import Celery

class Processor:


    def __init__(self, app, queue, name):
        self.name = name
        self.queue = queue
        self.app = app

    def __call__(self, *args, **kwargs):

        # Add logging callbacks in here
        return self.app.signature(self.name, args=args, queue=self.queue, kwargs=kwargs).delay()
