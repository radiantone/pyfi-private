"""
--config pyfi.conf.celery.Config
"""


class Config:
    """ """

    import configparser
    from pathlib import Path

    CONFIG = configparser.ConfigParser()

    HOME = str(Path.home())
    ini = HOME + "/pyfi.ini"
    CONFIG.read(ini)

    enable_utc = True
    timezone = "America/New_York"
    broker_url = CONFIG.get("broker", "uri")
    result_backend = CONFIG.get("backend", "uri")
