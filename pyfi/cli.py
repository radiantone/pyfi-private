"""
cli.py - pyfi CLI
"""
import functools
import socketserver
import click
import http
import logging
import pyfi.celery

from entangle.process import process
from pyfi.server import app
from pyfi.model import User, Flow, Processor, Node, Queue, Settings, Task, Log

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


DIRECTORY = "app/dist/spa"

Handler = functools.partial(
    http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)


@process
def run_http(port):
    import http.server

    PORT = port

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logging.info("Serving app on port", PORT)
        try:
            httpd.serve_forever()
        except:
            pass


@cli.command()
@click.option('--port', default=8000, help='Listen port')
def server(port):
    """
    Run pyfi server
    """
    import bjoern

    server = run_http(port+1)
    server(proc=True)
    click.echo("Serving API on port {}".format(port))
    try:
        bjoern.run(app, "127.0.0.1", port)
    except:
        pass
