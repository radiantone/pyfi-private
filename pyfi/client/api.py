"""
Python client API for invoking and building flows
"""
from .objects import Processor, Socket, Queue, Plug
from celery import group as parallel, chain as pipeline, chord as funnel, chunks as segment

def fork(*args, **kwargs):
    """ Execute the head function, pass that result to the body.
    Essentially the opposite of the chord. """
    head = args[0]
    body = args[1]

    result = head.delay()

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


__all__ = ('Processor', 'Socket', 'Queue', 'Plug',
           'parallel', 'pipeline', 'funnel', 'fork', 'segment')
