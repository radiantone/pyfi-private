"""
cli.py - pyfi CLI
"""
import functools
import socketserver
import click
import http
import logging
import signal

import pyfi.celery

from pyfi.server import app
from pyfi.model import User, Flow, Processor, Node, Queue, Settings, Task, Log


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    logging.info(f"Debug mode is {'on' if debug else 'off'}")


DIRECTORY = "app/dist/spa"

Handler = functools.partial(
    http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)


def run_http(port):
    """
    Run web server to serve UI
    """
    import http.server

    PORT = port

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logging.info("Serving app on port %s", PORT)

        def http_shutdown():
            """
            Handle any cleanup here
            """
            # Kill all processes
            httpd.shutdown()

        signal.signal(signal.SIGINT, http_shutdown)

        try:
            httpd.serve_forever()
        except:
            pass


@cli.command()
@click.option('--port', default=8000, help='Listen port')
def server(port):
    """
    Run pyfi API server
    """
    import bjoern
    from multiprocessing import Process

    process = Process(target=run_http, args=[port+1])
    process.start()
    logging.info("Serving API on port {}".format(port))

    try:
        bjoern.run(app, "0.0.0.0", port)
    except:
        logging.info("Shutting down...")
        process.terminate()
