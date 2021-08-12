from celery import Celery
from pyfi.config.celery import Config
from kombu import Exchange, Queue, binding

class Processor:
    """
    Docstring
    """

    def __init__(self, queue=None, name=None, config=None):
        from kombu.common import Broadcast

        self.queue = queue
        self.name = name
        self.app = Celery()
        if config is None:
            self.app.config_from_object(Config)
        else:
            self.app.config_from_object(config)

        if queue.find('topic') > -1:
            self.app.conf.task_queues = (
                Broadcast(queue, queue_arguments={
                    'x-message-ttl': 3000,
                    'x-expires': 30}),)

        else:
            self.queue = queue = Queue(
                queue,
                Exchange(queue, type='direct'),
                routing_key=name,
                expires=30,
                queue_arguments={
                    'x-message-ttl': 30000,
                    'x-expires': 30}
            )

        self.app.conf.task_routes = {
            name: {
                'queue': queue,
                'exchange': queue
            }
        }
        """


        self.app.conf.task_routes = {
            name: {
                'queue': queue,
                'exchange': queue
            }
        }

        """
    def __call__(self, *args, **kwargs):

        # Add logging callbacks in here
        kwargs['x-expires'] = 30
        return self.app.signature(self.name, args=args, queue=self.queue, kwargs=kwargs).delay()
