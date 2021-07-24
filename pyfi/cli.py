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
    context.obj['dburi'] = db

    app = init_app(db)
    database = model_init(app)
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
def init(context):

    try:
        context.obj['database'].create_all()
        logging.info("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)


@proc.command()
@click.argument('function', required=True)
@click.option('--schedule', required=True)
@click.option('--queue', required=True)
def start(function, schedule, queue):
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
def add():
    """
    Add an object to the database
    """
    pass


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
    logging.info("User %s[%s] added.", name, id)


@add.command()
@click.option('--id', default=None)
@click.option('-n', '--name', required=True)
@click.pass_context
def agent(context, id, name):
    """
    Add user object to the database
    """

    from uuid import uuid4

    if id is None:
        id = uuid4().hex

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
    Add user object to the database
    """

    from uuid import uuid4

    if id is None:
        id = uuid4().hex

    worker = Worker.query.filter_by(id=workerid).first()
    queue = Queue(name=name, id=id, worker_id=workerid)
    worker.queues += [queue]
    context.obj['database'].session.add(queue)
    context.obj['database'].session.add(worker)
    context.obj['database'].session.commit()
    logging.info("Queue %s[%s] added.", name, id)


@add.command()
@click.option('--id', default=None)
@click.option('-n', '--name', required=True, help="Name of worker")
@click.option('-c', '--concurrency', default=3, help='Number of worker tasks')
@click.option('-s', '--status', default='ready', help='Status string')
@click.option('-b', '--backend', default='redis://192.168.1.23', help='Message backend URI')
@click.option('-r', '--broker', default='pyamqp://192.168.1.23', help='Message broker URI')
@click.option('-h', '--hostname', default=hostname, help='Target server hostname')
@click.pass_context
def worker(context, id, name, concurrency, status, backend, broker, hostname):
    """
    Add a worker request
    """

    from pyfi.model import Processor
    from uuid import uuid4

    if id is None:
        id = uuid4().hex

    uuid = uuid4().hex
    processor = Processor(uuid=uuid, module='pyfi.tt')
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
    from pyfi.model import Processor
    from uuid import uuid4

    uuid = uuid4().hex
    processor = Processor(uuid=uuid, module='pyfi.tt')

    worker = Worker(module, host, concurrency)
    worker.processor = processor
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
    context.database.session.commit()
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
        print("{}:{}:{}".format(queue.id, queue.name, queue.worker_id))


@ls.command()
@click.pass_context
def users(context):
    """
    List users
    """

    users = User.query.all()
    for user in users:
        print("{}:{}".format(user.username, user.email))


@ls.command()
@click.pass_context
def workers(context):
    """
    List workers
    """

    workers = Worker.query.all()
    for _worker in workers:
        print("{}:{}:{}:{}:{}:{}:{} {}".format(_worker.id, _worker.name,
              _worker.concurrency, _worker.requested_status, _worker.processor, _worker.hostname, _worker.status, _worker.queues))


@ls.command()
@click.option('-d', '--db', default=POSTGRES, help='Database URI')
def processors(db):
    """
    List processors
    """

    app = init_app(db)
    database = model_init(app)

    processors = Processor.query.all()
    for processor in processors:
        print(processor)


@ls.command()
@click.pass_context
def agents():
    """
    List agents
    """
    agents = Agent.query.all()
    for agent in agents:
        print("{}:{}".format(agent.name, agent.id))


@cli.command()
@click.option('-p','--port', default=8000, help='Listen port')
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


@agent.command()
@click.option('-p','--port', default=8002, help='Listen port')
@click.option('-b','--backend', default='redis://192.168.1.23', help='Message backend URI')
@click.option('-r', '--broker', default='pyamqp://192.168.1.23', help='Message broker URI')
@click.pass_context
def start(context, port, backend, broker):
    """
    Run pyfi agent server
    """
    from pyfi.agent import Agent

    agent = Agent(context.obj['database'], port, backend=backend, broker=broker)

    agent.start()


@cli.command()
@click.option('-p','--port', default=8001, help='Listen port')
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
