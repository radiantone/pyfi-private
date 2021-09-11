"""
Python client API for invoking and building flows
"""
from celery.utils.functional import (is_list, lookahead, maybe_list, regen,
                                     seq_concat_item, seq_concat_seq)
from celery.utils.functional import _regen
from celery.utils import abstract
from celery.utils.objects import getitem_property
from .objects import Processor, Socket, Queue, Plug
from celery import group as parallel, chain as pipeline, chord as funnel, chunks as segment
from celery.canvas import Signature

def fork2(*args, **kwargs):
    """ Execute the head function, pass that result to the body.
    Essentially the opposite of the chord. """
    head = args[1]
    body = args[0]

    #result = head.delay().get()

    return parallel([g(head.delay().get()) for g in body])


class fork(parallel):


    def __init__(self, *tasks, **options):
        print("FORK INIT!", tasks, options)
        self.args = tasks
        self.kwargs = options
        #self.sig = parallel(*args[0])
        if len(tasks) == 1:
            tasks = tasks[0]
            if isinstance(tasks, parallel):
                tasks = tasks.tasks
            if isinstance(tasks, abstract.CallableSignature):
                tasks = [tasks.clone()]
            if not isinstance(tasks, _regen):
                tasks = regen(tasks)

        Signature.__init__(
            self, 'pyfi.fork', (), {'tasks': tasks}, **options
        )
        #self.subtask_type = 'group'

    def __call__(self, *partial_args, **options):
        print("FORK CALL!", partial_args, options)
        return self.apply_async(partial_args, **options)





'''
def chord(*args, **kwargs):
    from celery import group
    from celery import Celery
    import configparser
    from pathlib import Path

    CONFIG = configparser.ConfigParser()
    HOME = str(Path.home())
    ini = HOME+"/pyfi.ini"

    CONFIG.read(ini)

    backend = CONFIG.get('backend', 'uri')
    broker = CONFIG.get('broker', 'uri')
    app = Celery(backend=backend, broker=broker)
    print("CHORD APP",app)
    g = chord(*args)
    return g(app=app)
'''

__all__ = ('Processor', 'Socket', 'Queue', 'Plug',
           'parallel', 'pipeline', 'funnel', 'fork', 'segment')
