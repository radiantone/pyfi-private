"""
cli.py - pyfi CLI
"""
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import click
import logging
import socket

from pyfi.server import app
from pyfi.model import User, Agent, Worker, Action, Flow, Processor, Node, Queue, Settings, Task, Log, init_db as model_init
from pyfi.http import run_http

hostname = socket.gethostbyname(socket.gethostname())

POSTGRES = 'postgresql://postgres:pyfi101@'+hostname+':5432/pyfi'

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('-d', '--db', default=POSTGRES, help='Database URI')
@click.pass_context
def cli(context, debug, db):
    logging.debug(f"Debug mode is {'on' if debug else 'off'}")
    context.obj = {}

    # if db is None then check the .pyfi property file
    context.obj['dburi'] = db

    app = init_app(db)
    database = model_init(app)
    context.obj['app'] = app
    context.obj['database'] = database
    database.init_app(app)
    app.app_context().push()


def init_app(db):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()

    return app


def init_db(db):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database = SQLAlchemy(app)
    app.app_context().push()

    return database, app

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
@click.pass_context
def drop(context):
    """
    Drop all database tables
    """
    try:
        if click.confirm('Are you sure you want to drop the database?', default=False):
            if click.confirm('Are you REALLY sure you want to drop the database?', default=False):
                context.obj['database'].drop_all()
                print("Database dropped.")
            else:
                print("Operation aborted.")
        else:
            print("Operation aborted.")
    except Exception as ex:
        logging.error(ex)


@db.command()
@click.pass_context
def init(context):
    """
    Initialize database tables
    """
    try:
        context.obj['database'].create_all()
        logging.info("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)


@proc.command(name='start')
@click.argument('function', required=True)
@click.option('--schedule', required=True)
@click.option('--queue', required=True)
def start_processor(function, schedule, queue):
    """
    Start a processor
    """
    logging.info("Starting processor %s", function)
    # Run a worker with a beat cron schdule
    from celery import Celery
    from multiprocessing import Process

    celery = Celery('pyfi', backend='redis://192.168.1.23',
                    broker='pyamqp://192.168.1.23')

    @celery.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):

        # Executes every Monday morning at 7:30 a.m.
        """
        sender.add_periodic_task(
            crontab(hour=7, minute=30, day_of_week=1),
            test.s('Happy Mondays!'),
        )
        """
        # Add a wrapper task as the periodic task that retrieves
        # messages off a queue and dispatches it to the function
        pass


@cli.group()
@click.option('--id', default=None, help="ID of object being added")
@click.pass_context
def add(context, id):
    """
    Add an object to the databasepyfi 
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj['id'] = id


@cli.group()
def task():
    """
    Pyfi task management
    """
    pass


@task.command()
@click.argument('task', required=True)
def run(task):
    """
    Run a task
    """
    import importlib

    taskname = ''.join(task.rsplit('.')[-1])
    modulename = '.'.join(task.rsplit('.')[:-1])

    module = importlib.import_module(modulename)
    task = getattr(module, taskname)

    result = task.delay()

    print(result.get())


@add.command()
@click.argument('name')
@click.argument('email')
@click.pass_context
def user(context, name, email):
    """
    Add user object to the database
    """
    admin = User(username=name, email=email)
    context.obj['database'].session.add(admin)
    context.obj['database'].session.commit()
    logging.info("%s added.", user)


@add.command()
@click.option('--id', default=None)
@click.option('-n', '--name', required=True)
@click.pass_context
def agent(context, id, name):
    """
    Add agent object to the database
    """
    id = context.obj['id']

    agent = Agent(name=name, id=id)
    context.obj['database'].session.add(agent)
    context.obj['database'].session.commit()
    logging.info("Agent %s[%s] added.", name, id)


@add.command()
@click.option('-n','--name', required=True)
@click.option('--id', default=None)
@click.option('-w', '--workerid', required=True)
@click.pass_context
def queue(context, name, id, workerid):
    """
    Add queue object to the database
    """
    id = context.obj['id']

    worker = Worker.query.filter_by(id=workerid).first()
    queue = Queue(name=name, id=id, worker_id=workerid)
    worker.queues += [queue]
    context.obj['database'].session.add(queue)
    context.obj['database'].session.add(worker)
    context.obj['database'].session.commit()
    logging.info("Queue %s[%s] added.", name, id)


@add.command(name='worker')
@click.option('-n', '--name', required=True, help="Name of worker")
@click.option('-c', '--concurrency', default=3, help='Number of worker tasks')
@click.option('-s', '--status', default='ready', help='Status string')
@click.option('-b', '--backend', default='redis://192.168.1.23', help='Message backend URI')
@click.option('-r', '--broker', default='pyamqp://192.168.1.23', help='Message broker URI')
@click.option('-h', '--hostname', default=hostname, help='Target server hostname')
@click.pass_context
def add_worker(context, name, concurrency, status, backend, broker, hostname):
    """
    Add worker object to the database
    """
    from pyfi.model import Processor
    from uuid import uuid4

    uuid = uuid4()
    id = context.obj['id']

    processor = Processor(id=uuid, uuid=uuid, module='pyfi.tt')
    processor.name = 'processor'
    worker = Worker(id=id, name=name, processor=processor, concurrency=concurrency,
                    status='ready',
                    backend=backend,
                    broker=broker,
                    hostname=hostname,
                    requested_status=status)

    context.obj['database'].session.add(worker)
    context.obj['database'].session.commit()
    logging.info("Worker %s added.", name)


@cli.group()
def ls():
    """
    List database objects
    """
    pass


@cli.group()
def worker():
    """
    Run pyfi worker
    """
    pass


@worker.command()
@click.option('-h', '--host', default='worker@localhost', required=True)
@click.option('-m', '--module', required=True, multiple=True)
@click.option('-c', '--concurrency')
@click.pass_context
def start(context, host, module, concurrency):
    """
    Start a worker
    """
    from pyfi.worker import Worker

    worker = Worker(module, host, concurrency)
    worker.start()


@worker.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--procid', required=True)
@click.pass_context
def stop(context, host, procid, db):
    """
    Stop a worker
    """
    pass


@worker.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--procid', required=True)
@click.pass_context
def status(context, host, procid):
    """
    Get the status of a worker
    """
    pass


@worker.command()
@click.option('--id', required=True)
@click.option('-c', '--concurrency', default=3, help='Number of worker tasks')
@click.option('-s', '--status', default='ready', help='Status string')
@click.pass_context
def update(context, id, concurrency, status):
    """
    Update a worker
    """
    worker = Worker.query.filter_by(id=id).first()
    worker.concurrency = concurrency
    worker.requested_status = status
    context.obj['database'].session.add(worker)
    context.obj['database'].session.commit()
    logging.info("Worker %s updated.", id)

@cli.group()
def agent():
    """
    Run pyfi agent
    """
    pass


@ls.command()
@click.pass_context
def queues(context):
    """
    List queues
    """
    queues = Queue.query.all()
    for queue in queues:
        print(queue)


@ls.command()
@click.pass_context
def users(context):
    """
    List users
    """
    users = User.query.all()
    for user in users:
        print(user)


@ls.command()
@click.pass_context
def workers(context):
    """
    List workers
    """
    workers = Worker.query.all()
    for _worker in workers:
        print(_worker)

@ls.command()
@click.option('-d', '--db', default=POSTGRES, help='Database URI')
def processors(db):
    """
    List processors
    """
    processors = Processor.query.all()
    for processor in processors:
        print(processor)


@ls.command()
@click.pass_context
def agents(context):
    """
    List agents
    """
    agents = Agent.query.all()
    for agent in agents:
        print(agent)


@cli.group()
def api():
    pass


@api.command(name='start')
@click.option('-ip', default=hostname, help='IP bind address')
@click.option('-p', '--port', default=8000, help='Listen port')
@click.pass_context
def api_start(context, ip, port):
    """
    Run pyfi API server
    """
    import bjoern
    from pyfi.server import app as server
    logging.info("Initializing server app....")
    init_db(server)
    logging.info("Serving API on {}:{}".format(ip,port))

    try:
        bjoern.run(server, ip, port)
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")


@agent.command(name='start')
@click.option('-p','--port', default=8002, help='Listen port')
@click.option('-b','--backend', default='redis://192.168.1.23', help='Message backend URI')
@click.option('-r', '--broker', default='pyamqp://192.168.1.23', help='Message broker URI')
@click.pass_context
def start_agent(context, port, backend, broker):
    """
    Run pyfi agent server
    """
    from pyfi.agent import Agent

    agent = Agent(context.obj['database'], port, backend=backend, broker=broker)

    agent.start()


@cli.group()
@click.pass_context
def web(context):
    pass

@web.command(name='start')
@click.option('-p','--port', default=8001, help='Listen port')
def web_start(port):
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
