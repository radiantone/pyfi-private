"""
--config pyfi.conf.celery.Config
"""
class Config:
    """
    
    """
    enable_utc = True
    timezone = 'America/New_York'
    broker_url = 'pyamqp://192.168.1.23'
    result_backend = None #'redis://192.168.1.23'
