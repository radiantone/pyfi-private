"""
cli.py - pyfi CLI
"""
import click
import logging


from pyfi.server import app
from pyfi.model import User, Flow, Processor, Node, Queue, Settings, Task, Log, db
from pyfi.http import run_http

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    logging.debug(f"Debug mode is {'on' if debug else 'off'}")


@cli.group()
def processor():
    """
    Processor lifecycle commands
    """
    pass


@processor.command()
@click.argument('package')
def start(package):
    logging.info("Starting processor %s", package)

@cli.group()
def add():
    """
    Add an object to the database
    """
    pass


@add.command()
@click.argument('name')
@click.argument('email')
def user(name, email):
    """
    Add user object to the database
    """
    admin = User(username=name, email=email)
    db.session.add(admin)
    db.session.commit()

@cli.group()
def ls():
    """
    List resources
    """
    pass

@ls.command()
def queues():
    """
    List queues
    """
    logging.info("ls queues")


@ls.command()
def users():
    """
    List queues
    """
    users = User.query.all()
    for user in users:
        print("{}:{}".format(user.username,user.email))

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
