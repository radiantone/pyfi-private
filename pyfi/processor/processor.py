from celery import Celery
from celery.local import class_property
from pyfi.config.celery import Config

class Processor:
    """
    Docstring
    """

    def __init__(self, queue=None, name=None, config=None):
        self.queue = queue
        self.name = name
        self.app = Celery()
        if config is None:
            self.app.config_from_object(Config)
        else:
            self.app.config_from_object(config)


    def __call__(self, *args, **kwargs):

        # Add logging callbacks in here
        return self.app.signature(self.name, args=args, queue=self.queue, kwargs=kwargs).delay()
