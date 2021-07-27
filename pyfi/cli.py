"""
cli.py - pyfi CLI command tools
"""
from werkzeug.utils import cached_property
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import click
import logging
import socket

import pyfi.db.postgres
from pyfi.server import app
from pyfi.db.model import UserModel, AgentModel, WorkerModel, ActionModel, FlowModel, ProcessorModel, NodeModel, QueueModel, SettingsModel, TaskModel, LogModel, init_db as model_init
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

    try:
        app = init_app(db)
        database = model_init(app)
        context.obj['app'] = app
        context.obj['database'] = database
        database.init_app(app)
        app.app_context().push()
    except:
        import traceback
        print(traceback.format_exc())


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
@click.option('--id', default=None, help="ID of processor")
@click.pass_context
def proc(context, id):
    """
    Run or manage processors
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj['id'] = str(id)


@cli.group()
@click.pass_context
def db(context):
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
@click.option('-d', '--db', default= 'postgresql://postgres:pyfi101@'+hostname+':5432/postgres', help='Database URI')
@click.pass_context
def init(context, db):
    """
    Initialize database tables
    """
    try:
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker

            engine = create_engine(db)
            session = sessionmaker(bind=engine)()
            session.connection().connection.set_isolation_level(0)
            session.execute('CREATE DATABASE pyfi')
            session.connection().connection.set_isolation_level(1)
            print("Database created")
            app = init_app(POSTGRES)
            database = model_init(app)
            context.obj['app'] = app
            context.obj['database'] = database
            database.init_app(app)
            app.app_context().push()
            print("App created")
        except:
            pass
        context.obj['database'].create_all()
        logging.info("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)


@proc.command(name='remove')
@click.pass_context
def remove_processor(context):
    """
    Remove a processor
    """
    processor = ProcessorModel.query.filter_by(id=context.obj['id']).first()
    # Business logic here?
    processor.requested_status = 'removed'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor remove requested.")


@proc.command(name='stop')
@click.pass_context
def stop_processor(context):
    """
    Stop a processor
    """
    print("Stopping ", context.obj['id'])
    processor = ProcessorModel.query.filter_by(id=context.obj['id']).first()
    # Business logic here?
    processor.requested_status = 'stopped'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor stop requested.")


@proc.command(name='start')
@click.pass_context
def start_processor(context):
    """
    Start a processor
    """
    processor = ProcessorModel.query.filter_by(id=context.obj['id']).first()
    # Business logic here?
    processor.requested_status = 'started'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor start requested.")


@proc.command(name='restart')
@click.pass_context
def restart_processor(context):
    """
    Retart a processor
    """
    processor = ProcessorModel.query.filter_by(id=context.obj['id']).first()
    # Business logic here?
    processor.requested_status = 'restart'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor restart requested.")


@cli.group()
@click.option('--id', default=None, help="ID of object being added")
@click.pass_context
def add(context, id):
    """
    Add an object to the database
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj['id'] = str(id)


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


@add.command(name='processor')
@click.option('-n', '--name', required=True)
@click.option('-m', '--module', required=True)
@click.option('-h', '--hostname', default=hostname, help='Target server hostname')
@click.option('-t', '--tasks', default=3, help='Number of worker tasks')
@click.option('-g', '--gitrepo', default=None, help='Git repo URI')
@click.option('-c', '--commit', default=None, help='Git commit id for processor code')
@click.option('-s', '--requested_status', default='ready', required=False)
@click.pass_context
def add_processor(context, name, module, hostname, tasks, gitrepo, commit, requested_status):
    """
    Add processor to the database
    """
    id = context.obj['id']
    processor = ProcessorModel(
        id=id, status='ready', hostname=hostname, gitrepo=gitrepo, commit=commit, concurrency=tasks, requested_status=requested_status, name=name, module=module)

    processor.updated = func.now()
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(processor)


@add.command()
@click.option('-n', '--name', required=True)
@click.option('-e', '--email', required=True)
@click.pass_context
def user(context, name, email):
    """
    Add user object to the database
    """
    id = context.obj['id']
    user = UserModel(id=id, username=name, email=email)

    user.updated = func.now()
    context.obj['database'].session.add(user)
    context.obj['database'].session.commit()
    print(user)


@add.command(name='agent')
@click.option('-n', '--name', required=True)
@click.pass_context
def add_agent(context, name):
    """
    Add agent object to the database
    """
    id = context.obj['id']

    agent = AgentModel(name=name, id=id)
    agent.updated = func.now()
    context.obj['database'].session.add(agent)
    context.obj['database'].session.commit()
    print(agent)


@add.command()
@click.option('-n','--name', required=True)
@click.option('-p', '--procid', required=True)
@click.pass_context
def queue(context, name, procid):
    """
    Add queue object to the database
    """
    id = context.obj['id']

    processor = ProcessorModel.query.filter_by(id=procid).first()
    queue = QueueModel(name=name, id=id, requested_status='create',
                       status='ready', processor_id=procid)

    queue.updated = func.now()
    processor.queues += [queue]
    context.obj['database'].session.add(queue)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(queue)

@cli.group()
def ls():
    """
    List database objects
    """
    pass


@cli.group()
def get():
    """
    Get unique row
    """
    pass


@get.command(name='queue')
@click.pass_context
def get_queue(context):
    queue = QueueModel.query.with_for_update(of=QueueModel).filter_by(requested_status='create').first()
    if queue is not None:
        queue.requested_status = 'ready'
        queue.status = 'created'
        print(queue)
        if click.confirm('Continue ?', default=False):
            pass
        context.obj['database'].session.commit()


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
    queues = QueueModel.query.all()
    for queue in queues:
        print(queue)


@ls.command()
@click.pass_context
def users(context):
    """
    List users
    """
    users = UserModel.query.all()
    for user in users:
        print(user)


@ls.command()
@click.pass_context
def workers(context):
    """
    List workers
    """
    workers = WorkerModel.query.all()
    for _worker in workers:
        print(_worker)

@ls.command()
@click.option('-d', '--db', default=POSTGRES, help='Database URI')
def processors(db):
    """
    List processors
    """
    processors = ProcessorModel.query.all()
    for processor in processors:
        print(processor)


@ls.command()
@click.pass_context
def agents(context):
    """
    List agents
    """
    agents = AgentModel.query.all()
    for agent in agents:
        print(agent)


@cli.group()
def api():
    """
    API server admin
    """
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
    logging.info("Serving API on {}:{}".format(ip, port))

    from pyfi.api import blueprint

    server.register_blueprint(blueprint)

    server.app_context().push()
    try:
        bjoern.run(server, ip, port)
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")


@agent.command(name='start')
@click.option('-p','--port', default=8002, help='Listen port')
@click.option('-b','--backend', default='redis://192.168.1.23', help='Message backend URI')
@click.option('-r', '--broker', default='pyamqp://192.168.1.23', help='Message broker URI')
@click.option('-q', '--queues', is_flag=True, help='Run the queue monitor only')
@click.pass_context
def start_agent(context, port, backend, broker, queues):
    """
    Run pyfi agent server
    """
    from pyfi.agent import Agent
    from pyfi.db.model import init_db

    agent = Agent(context.obj['database'], port, backend=backend, broker=broker)
    init_db(context.obj['app'])
    agent.start(queues)


@cli.group()
@click.pass_context
def web(context):
    """
    Web server admin
    """
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
