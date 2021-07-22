from celery import Celery

celery = Celery('pyfi', backend='redis://localhost', broker='pyamqp://')


@celery.task
def shout():
    print("WORKER SHOUT!")
