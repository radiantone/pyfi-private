"""
Pyfi harness tasks for moving data and invoking processor functions.
This is the meta layer that wraps all the processor code. It handles a variety of
things such as security, logging, message dispatching, enqueing/dequeuing, error handling and more.

"""
from celery import Celery

celery = Celery('pyfi', backend='redis://192.168.1.23',
                broker='pyamqp://192.168.1.23')

@celery.task
def add(x, y):
    """
    Docstring
    """
    return x + y


"""
TBD pyfi wrapper tasks
"""
