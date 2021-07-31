"""
cli.py - pyfi CLI command tools
"""
import logging
from pyfi.db.model.models import PlugModel
import socket
from datetime import datetime

import click

from flask import Flask

import pyfi.db.postgres
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from pyfi.server import app
from pyfi.db.model import UserModel, AgentModel, WorkerModel,PlugModel, OutletModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel
from pyfi.web import run_http

hostname = socket.gethostbyname(socket.gethostname())

POSTGRES = 'postgresql://postgres:pyfi101@'+hostname+':5432/pyfi'

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('-d', '--db', default=POSTGRES, help='Database URI')
@click.pass_context
def cli(context, debug, db):
    """
    Pyfi CLI for managing the pyfi network
    """
    context.obj = {}

    # if db is None then check the .pyfi property file
    context.obj['dburi'] = db

    try:
        engine = create_engine(db)
        engine.uri = db
        session = sessionmaker(bind=engine)()
        context.obj['database'] = engine
        context.obj['session'] = session
        engine.session = session
    except:
        import traceback
        print(traceback.format_exc())


@cli.group()
@click.pass_context
def update(context):
    """
    Update a database object
    """
    pass


@cli.group()
@click.pass_context
def node(context):
    """
    Node management operations
    """
    pass


@node.command()
@click.option('-t', '--to', required=True)
@click.pass_context
def clone(context, to):
    """
    Clone the current virtual environment to the node host --to
    """
    pass


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
def migrate(context):
    """
    Perform database migration/upgrade
    """
    #db_migrate(directory='migration')
    #migrate_upgrade(directory='migration')
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
                from pyfi.db.model import Base
                for t in Base.metadata.sorted_tables:
                    t.drop(context.obj['database'])
                    print("Dropped {}".format(t.name))
                print("Database dropped.")
            else:
                print("Operation aborted.")
        else:
            print("Operation aborted.")
    except Exception as ex:
        logging.error(ex)


@db.command(name='init')
@click.option('-d', '--db', default= 'postgresql://postgres:pyfi101@'+hostname+':5432/postgres', help='Database URI')
@click.pass_context
def db_init(context, db):
    """
    Initialize database tables
    """
    try:
        try:
            from sqlalchemy import create_engine

            session = context.obj['session']
            session.connection().connection.set_isolation_level(0)
            session.execute('CREATE DATABASE pyfi')
            session.connection().connection.set_isolation_level(1)
            print("Database created")
        except:
            pass
        
        from pyfi.db.model import Base

        Base.metadata.create_all(context.obj['database'])
        #context.obj['database'].create_all()
        logging.info("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)


@proc.command(name='remove')
@click.pass_context
def remove_processor(context):
    """
    Remove a processor
    """
    processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=context.obj['id']).first()
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
    processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=context.obj['id']).first()
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
    processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=context.obj['id']).first()
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
    processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=context.obj['id']).first()
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
@click.option('--id', default=None, help="ID of object being added")
@click.pass_context
def update(context, id):
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


def update_object(obj, locals):

    for var in locals.keys():
        if locals[var] is not None and var != 'id':
            setattr(obj,var,locals[var])

    obj.updated = datetime.now()
    return obj

@update.command(name='processor')
@click.option('-n', '--name', default=None, required=False)
@click.option('-m', '--module', default=None, required=False)
@click.option('-t', '--task', default=None, required=False)
@click.option('-h', '--hostname', default=None, help='Target server hostname')
@click.option('-w', '--workers', default=None, help='Number of worker tasks')
@click.option('-g', '--gitrepo', default=None, help='Git repo URI')
@click.option('-c', '--commit', default=None, help='Git commit id for processor code')
@click.option('-r', '--requested_status', default=None, required=False)
@click.option('-s', '--schedule', default=None, required=False)
@click.option('-b', '--beat', default=None, is_flag=True, required=False)
@click.option('-br', '--branch', default=None, required=False)
@click.pass_context
def update_processor(context, name, module, task, hostname, workers, gitrepo, commit, requested_status, schedule, beat, branch):
    """
    Update a processor in the database
    """
    import inspect
    id = context.obj['id']

    if name is not None:
        processor = context.obj['database'].session.query(ProcessorModel).filter_by(name=name).first()
        print("old ",processor)
    elif id is not None:
        processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=id).first()

    argspec = inspect.getargvalues(inspect.currentframe())
    _locals = argspec.locals
    processor = update_object(processor, _locals)

    print("new ",processor)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()


@add.command(name='processor')
@click.option('-n', '--name', required=True)
@click.option('-m', '--module', required=True)
@click.option('-t', '--task', required=True)
@click.option('-h', '--hostname', default=hostname, help='Target server hostname')
@click.option('-w', '--workers', default=3, help='Number of worker tasks')
@click.option('-g', '--gitrepo', default=None, help='Git repo URI')
@click.option('-c', '--commit', default=None, help='Git commit id for processor code')
@click.option('-r', '--requested_status', default='ready', required=False)
@click.option('-s', '--schedule', default=10, required=False)
@click.option('-b', '--beat', default=False, is_flag=True, required=False)
@click.option('-br', '--branch', default='main', required=False)
@click.pass_context
def add_processor(context, name, module, task, hostname, workers, gitrepo, commit, requested_status, schedule, beat, branch):
    """
    Add processor to the database
    """
    id = context.obj['id']
    processor = ProcessorModel(
        id=id, status='ready', hostname=hostname, task=task, schedule=schedule, branch=branch, gitrepo=gitrepo, beat=beat, commit=commit, concurrency=workers, requested_status=requested_status, name=name, module=module)

    processor.updated = datetime.now()
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

    user.updated = datetime.now()
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
    agent.updated = datetime.now()
    context.obj['database'].session.add(agent)
    context.obj['database'].session.commit()
    print(agent)


@add.command(name='role')
@click.option('-n', '--name', required=True)
@click.pass_context
def add_role(context, name):
    """
    Add role object to the database
    """
    id = context.obj['id']

    role = RoleModel(name=name, id=id)
    role.updated = datetime.now()
    context.obj['database'].session.add(role)
    context.obj['database'].session.commit()
    print(role)


@add.command(name='queue')
@click.option('-n','--name', required=True)
@click.pass_context
def add_queue(context, name):
    """
    Add queue object to the database
    """
    id = context.obj['id']

    queue = QueueModel(name=name, id=id, requested_status='create',
                       status='ready')

    queue.updated = datetime.now()
    context.obj['database'].session.add(queue)
    context.obj['database'].session.commit()
    print(queue)


@update.command(name='plug')
@click.option('-n', '--name', required=True)
@click.option('-q', '--queue', required=True, help="Queue name")
@click.option('-pi', '--procid', default=None, required=False, help="Processor id")
@click.option('-pn', '--procname', default=None, required=False, help="Processor name")
@click.pass_context
def update_plug(context, name, queue, procid, procname):
    """
    Update or move a processor plug
    """
    import inspect
    id = context.obj['id']

    # Get the named or id of the plug model
    if name is not None:
        plug = PlugModel.query.filter_by(name=name).first()
    elif id is not None:
        plug = PlugModel.query.filter_by(id=id).first()

    # Get the plug's current processor
    current_processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=plug.processor_id).first()

    # Get the processor referenced in the CLI
    if procname is not None:
        new_processor = context.obj['database'].session.query(ProcessorModel).filter_by(name=procname).first()
    elif procid is not None:
        new_processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=procid).first()

    # If the new processor is different, then add it to the transaction
    if new_processor.id != current_processor.id:
        context.obj['database'].session.add(new_processor)

    # Update all the values in the plug object
    argspec = inspect.getargvalues(inspect.currentframe())
    _locals = argspec.locals
    plug = update_object(plug, _locals)

    # Remap the plug relation in the current processor
    # if this plug has been moved to a new processor
    new_plugs = []
    for _plug in current_processor.plugs:
        if _plug.id != plug.id:
            new_plugs += [_plug]

    current_processor.plugs = new_plugs

    context.obj['database'].session.add(plug)
    context.obj['database'].session.add(current_processor)
    context.obj['database'].session.commit()
    print(plug)


@add.command(name='plug')
@click.option('-n', '--name', required=True)
@click.option('-q', '--queue', required=True, help="Queue name")
@click.option('-pi', '--procid', default=None, required=False, help="Processor id")
@click.option('-pn', '--procname', default=None, required=False, help="Processor name")
@click.pass_context
def add_plug(context, name, queue, procid, procname):
    """
    Add plug to a processor
    """
    id = context.obj['id']

    if procname is not None:
        processor = context.obj['database'].session.query(ProcessorModel).filter_by(name=procname).first()
    elif procid is not None:
        processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=procid).first()

    queue = context.obj['database'].session.query(QueueModel).filter_by(name=queue).first()
    plug = PlugModel(name=name, id=id, requested_status='create',
                       status='ready', processor_id=procid)
    plug.queue = queue
    plug.updated = datetime.now()
    processor.plugs += [plug]
    context.obj['database'].session.add(plug)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(plug)


@add.command(name='outlet')
@click.option('-n', '--name', required=True)
@click.option('-q', '--queue', required=True, help="Queue name")
@click.option('-pi', '--procid', default=None, required=False, help="Processor id")
@click.option('-pn', '--procname', default=None, required=False, help="Processor name")
@click.pass_context
def add_outlet(context, name, queue, procid, procname):
    """
    Add outlet to a processor
    """
    id = context.obj['id']

    if procname is not None:
        processor = context.obj['database'].session.query(ProcessorModel).filter_by(name=procname).first()
    elif procid is not None:
        processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=procid).first()

    queue = context.obj['database'].session.query(
        QueueModel).filter_by(name=queue).first()
    outlet = OutletModel(name=name, id=id, requested_status='create',
                       status='ready', processor_id=procid)
    outlet.queue = queue
    outlet.updated = datetime.now()
    processor.outlets += [outlet]
    context.obj['database'].session.add(outlet)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(outlet) 


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
def nodes(context):
    """
    List queues
    """
    nodes = context.obj['database'].session.query(NodeModel).all()
    for node in nodes:
        print(node)


@ls.command()
@click.pass_context
def queues(context):
    """
    List queues
    """
    queues = context.obj['database'].session.query(QueueModel).all()
    for queue in queues:
        print(queue)


@ls.command()
@click.pass_context
def users(context):
    """
    List users
    """
    users = context.obj['database'].session.query(UserModel).all()
    for user in users:
        print(user)


@ls.command()
@click.pass_context
def workers(context):
    """
    List workers
    """
    
    workers = context.obj['database'].session.query(WorkerModel).all()
    for _worker in workers:
        print(_worker)


@ls.command()
@click.option('-d', '--db', default=POSTGRES, help='Database URI')
@click.pass_context
def processors(context, db):
    """
    List processors
    """
    processors = context.obj['database'].session.query(ProcessorModel).all()
    for processor in processors:
        print(processor)


@ls.command()
@click.pass_context
def agents(context):
    """
    List agents
    """
    agents = context.obj['database'].session.query(AgentModel).all()
    for agent in agents:
        print(agent)


@ls.command()
@click.pass_context
def outlets(context):
    """
    List agents
    """
    agents = context.obj['database'].session.query(OutletModel).all()
    for agent in agents:
        print(agent)


@ls.command()
@click.pass_context
def plugs(context):
    """
    List agents
    """
    agents = context.obj['database'].session.query(PlugModel).all()
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

    agent = Agent(context.obj['database'], port, backend=backend, broker=broker)
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
