"""
cli.py - pyfi CLI
"""
import click
import logging


from pyfi.server import app
from pyfi.agent import app as agentapp
from pyfi.model import User, Agent, Flow, Processor, Node, Queue, Settings, Task, Log, db as database
from pyfi.http import run_http


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    logging.debug(f"Debug mode is {'on' if debug else 'off'}")


@cli.group()
def proc():
    """
    Run or manage processors
    """
    pass


@cli.group()
def db():
    """
    Database operations
    """
    pass


@db.command()
def init():
    from flask import Flask

    try:
        app = Flask(__name__)

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        database.init_app(app)
        app.app_context().push()
        database.create_all()
        logging.info("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)

@proc.command()
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
    database.session.add(admin)
    database.session.commit()
    logging.info("User %s added.", name)


@add.command()
@click.argument('name')
@click.argument('id')
def agent(name, id):
    """
    Add user object to the database
    """
    agent = Agent(name=name, id=id)
    database.session.add(agent)
    database.session.commit()
    logging.info("Agent %s added.",name)

@cli.group()
def ls():
    """
    List database objects
    """
    pass


@cli.group()
def agent():
    """
    Run pyfi agent
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


@ls.command()
def agents():
    """
    List queues
    """
    agents = Agent.query.all()
    for agent in agents:
        print("{}:{}".format(agent.name, agent.id))


@cli.command()
@click.option('--port', default=8000, help='Listen port')
def api(port):
    """
    Run pyfi API server
    """
    import bjoern
    logging.info("Serving API on port {}".format(port))

    try:
        bjoern.run(app, "0.0.0.0", port)
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")


@cli.command()
@click.option('--port', default=8002, help='Listen port')
@click.option('--database', default='sqlite:////tmp/test.db', help='Listen port')
def agent(port, database):
    """
    Run pyfi agent server
    """
    import bjoern
    logging.info("Serving agent on port {}".format(port))
    agentapp.config['SQLALCHEMY_DATABASE_URI'] = database

    # Create database ping thread to notify pyfi that I'm here and active

    try:
        bjoern.run(agentapp, "0.0.0.0", port)
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")

@cli.command()
@click.option('--port', default=8001, help='Listen port')
def web(port):
    """
    Run pyfi test web server
    """

    from multiprocessing import Process

    try:
        process = Process(target=run_http, args=[port])
        process.start()
        process.join()
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")

