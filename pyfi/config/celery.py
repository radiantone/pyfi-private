"""
--config pyfi.conf.celery.Config
"""


class Config:
    """

    """
    enable_utc = True
    timezone = 'America/New_York'
    broker_url = 'pyamqp://phoenix'
    result_backend = None  # 'redis://phoenix'
