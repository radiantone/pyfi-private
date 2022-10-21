import configparser
import logging
from pathlib import Path

from celery import Celery

from pyfi.client.user import USER

from .objects import Socket

CONFIG = configparser.ConfigParser()
HOME = str(Path.home())

ini = HOME + "/pyfi.ini"

CONFIG.read(ini)


class TheMeta(type):
    def __new__(meta, name, bases, attributes):
        # Check if args contains the number "42"
        # or has the string "The answer to life, the universe, and everything"
        # If so, just return a pointer to an existing object:
        # Else, just create the object as it is:
        return super(TheMeta, meta).__new__(meta, name, bases, attributes)

    def __init__(cls, name, bases, dct):
        logging.debug("TheMeta init")
        super(TheMeta, cls).__init__(name, bases, dct)


class ProcessorBase:
    __metaclass__ = TheMeta

    def __init__(self):
        import types

        logging.debug("ProcessorBase init")
        logging.debug("ProcessorBase: sockets: %s", self.__sockets__)
        for socket in self.__sockets__:

            def wait(self, *args, taskid=None):
                """Retrive result for task"""
                from celery.result import AsyncResult

                backend = CONFIG.get("backend", "uri")
                broker = CONFIG.get("broker", "uri")
                app = Celery(backend=backend, broker=broker)
                from ..util import config

                app.config_from_object(config)
                """ Given the taskid, return an asynchronous result """
                res = AsyncResult(taskid, app=app)

                return res

            def socket_dispatch(*args, **kwargs):
                """In place of the original class method, dispatch to the socket"""
                logging.debug("socket_dispatch")
                _sock = Socket(name=socket.name, user=USER).p
                return _sock

            _function = types.MethodType(socket_dispatch, self)
            _sock = Socket(name=socket.name, user=USER)
            _wait = types.MethodType(wait, _sock)
            setattr(_sock, "get", _wait)
            setattr(self, socket.task.name, _sock)


class HTTPProcessor(ProcessorBase):
    def __init__(self, *args):
        logging.debug("HTTPProcessor init")
        super(HTTPProcessor, self).__init__(*args)

    def http_get(self, *args, **kwargs):
        logging.info("http_get %s %s", args, kwargs)
