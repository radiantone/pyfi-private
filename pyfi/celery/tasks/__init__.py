from celery import Celery

celery = Celery('pyfi', backend='redis://localhost', broker='pyamqp://')

@celery.task
def add(x, y):
    return x + y
