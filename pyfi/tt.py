from celery import Celery

celery = Celery('pyfi', backend='redis://192.168.1.23',
                broker='pyamqp://192.168.1.23')

@celery.task
def see():
   print("I see TT!")
   return "I see TT!"
