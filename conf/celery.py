"""
--config pyfi.conf.celery.Config
"""
class Config:
    """
    
    """
    enable_utc = True
    timezone = 'America/New_York'
    broker_url = 'pyamqp://192.168.1.23'

    ## Using the database to store task state and results.
    result_backend = 'postgresql://postgres:pyfi101@192.168.1.23:5432/pyfi'