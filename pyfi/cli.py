"""
cli.py - pyfi CLI command tool for managing database
"""
import getpass
import configparser
from pathlib import Path
import logging
import os
from pyfi.db.model.models import PrivilegeModel
import sys
from datetime import datetime

import click

from flask import Flask

import pyfi.db.postgres
from sqlalchemy import create_engine, MetaData, literal_column
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from pyfi.server import app
from pyfi.db.model import SchedulerModel, UserModel, AgentModel, WorkerModel, CallModel, PlugModel, SocketModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel
from pyfi.web import run_http

import platform
HOSTNAME = platform.node()

current_user = getpass.getuser()

POSTGRES_ROOT = 'postgresql://postgres:pyfi101@'+HOSTNAME+':5432/'
POSTGRES = 'postgresql://postgres:pyfi101@'+HOSTNAME+':5432/pyfi'

home = str(Path.home())

CONFIG = configparser.ConfigParser()

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

@click.group(invoke_without_command=True)
@click.option('--debug', is_flag=True, default=False, help='Debug switch')
@click.option('-d', '--db', help='Database URI')
@click.option('--backend', help='Task queue backend')
@click.option('--broker', help='Message broker URI')
@click.option('-i', '--ini', default=home+"/pyfi.ini", help='PYFI .ini configuration file')
@click.option('-c', '--config', default=False, is_flag=True, help='Configure pyfi')
@click.pass_context
def cli(context, debug, db, backend, broker, ini, config):
    """
    Pyfi CLI for managing the pyfi network
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    if debug:
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    context.obj = {}
    if config:
        if not db:
            db = click.prompt('Database connection URI',
                              type=str, default=POSTGRES)
        if not backend:
            backend = click.prompt('Result backend URI',
                                   type=str, default='redis://localhost')
        if not broker:
            broker = click.prompt('Message broker URI',
                                  type=str, default='pyamqp://localhost')

        _config = configparser.ConfigParser()
        _config.add_section('database')
        _config.set('database', 'uri', db)

        _config.add_section('backend')
        _config.set('backend', 'uri', backend)

        _config.add_section('broker')
        _config.set('broker', 'uri', broker)
        with open(home+"/pyfi.ini", "w") as configfile:
            _config.write(configfile)

        print("Configuration file created at {}".format(home+"/pyfi.ini"))
        

    if not os.path.exists(ini) and db is None:
        print("No database uri configured. Please run \033[1m $ pyfi --config")
        exit(1)

    if os.path.exists(ini) and db is None:
        CONFIG.read(ini)
        db = CONFIG.get('database', 'uri')

    # If there is a pyfi.ini file in users home directory
    # if db is None then check the .pyfi property file
    context.obj['dburi'] = db
    try:
        engine = create_engine(db)
        engine.uri = db
        session = sessionmaker(bind=engine)()
        context.obj['database'] = engine
        context.obj['session'] = session
        engine.session = session

        context.obj['owner'] = session.query(
            literal_column("current_user")).first()[0]

    except:
        #import traceback
        #print(traceback.format_exc())
        print("Database unavailable. Please check your configuration or ensure database server is running.")
        return

    if len(sys.argv) == 1:
        click.echo(context.get_help())


@cli.group()
@click.pass_context
def update(context):
    """
    Update a database object
    """


@cli.group()
@click.pass_context
def node(context):
    """
    Node management operations
    """


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
@click.option('-d', '--directory', default='migrations', help="Directory of migration pyfi agent")
@click.pass_context
def migrate(context, directory):
    """
    Perform database migration/upgrade
    """
    from pyfi.db.model import Base
    from alembic.migration import MigrationContext
    from alembic.autogenerate import compare_metadata, produce_migrations
    from alembic.config import Config

    target_metadata = Base.metadata

    engine = context.obj['database']

    mc = MigrationContext.configure(engine.connect())
    diff = compare_metadata(mc, target_metadata)
    script = produce_migrations(mc, target_metadata)

    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('script_location', directory)
    alembic_cfg.set_main_option('sqlalchemy.url', context.obj['dburi'])
    command.upgrade(alembic_cfg, 'head')


@db.command(help="Drop and rebuild database tables")
@click.option('-y', '--yes', is_flag=True, prompt=True, help="Yes to rebuild now")
@click.pass_context
def rebuild(context, yes):

    if yes:
        dropdb(context)
        context.invoke(db_init)

def dropdb(context):
    from pyfi.db.model import Base

    # For every user in "user" table, DROP USER name

    _users = [u.name for u in context.obj['database'].session.query(
        UserModel).all()]
    context.obj['database'].session.commit()
    for t in Base.metadata.sorted_tables:
        try:
            t.drop(context.obj['database'])
            print("Dropped {}".format(t.name))
        except:
            pass


    context.obj['database'].session.commit()
    for user in _users:
        context.obj['database'].session.execute(
            f"DROP OWNED BY {user}")
        context.obj['database'].session.execute(
            f"DROP USER {user}")
        print("Dropped user {}".format(user))

    context.obj['database'].session.commit()
    print("Database dropped.")
            

@db.command(name='drop')
@click.option('-y', '--yes', is_flag=True, default=False, help="Yes to rebuild without prompting")
@click.pass_context
def db_drop(context, yes):
    """
    Drop all database tables
    """
    try:
        if not yes:
            if click.confirm('Are you sure you want to drop the database?', default=False):
                if click.confirm('Are you REALLY sure you want to drop the database?', default=False):
                    dropdb(context)
                else:
                    print("Operation aborted.")
            else:
                print("Operation aborted.")

        # Drop roles
    except Exception as ex:
        logging.error(ex)

@db.command(name='json', help="Dump the database to JSON")
@click.pass_context
def db_json(context):
    """
    Dump database to JSON
    """
    import json

    """ Returns the entire content of a database as lists of dicts"""
    engine = context.obj['database']
    meta = MetaData()
    meta.reflect(bind=engine)  # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html
    result = {}
    for table in meta.sorted_tables:
        result[table.name] = [dict(row) for row in engine.execute(table.select())]
    print(json.dumps(result, indent=4, default=str))

@db.command(name='init')
@click.pass_context
def db_init(context):
    """
    Initialize database tables
    """
    try:
        try:
            from sqlalchemy import create_engine
            engine = create_engine(POSTGRES_ROOT+'postgres')
            session = sessionmaker(bind=engine)()
            session.connection().connection.set_isolation_level(0)
            session.execute('CREATE DATABASE pyfi')
            session.connection().connection.set_isolation_level(1)
            print("Database created")
            engine = create_engine(context.obj['dburi'])
            engine.uri = db
            session = sessionmaker(bind=engine)()
            session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            context.obj['database'] = engine
            context.obj['session'] = session
            engine.session = session
        except:
            pass

        from pyfi.db.model import Base

        Base.metadata.create_all(context.obj['database'])
        for t in Base.metadata.sorted_tables:
            try:
                sql = f"ALTER TABLE \"{t.name}\" ENABLE ROW LEVEL SECURITY"
                print("Enabling security on table {}".format(t.name))
                context.obj['database'].session.execute(sql)
                sql = f"CREATE POLICY {t.name}_security ON \"{t.name}\" USING ({t.name}.owner::text = current_user)"
                context.obj['database'].session.execute(sql)
            except:
                pass

            context.obj['session'].commit()
        print("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)


@proc.command(name='remove')
@click.pass_context
def remove_processor(context):
    """
    Remove a processor
    """
    processor = context.obj['database'].session.query(
        ProcessorModel).filter_by(id=context.obj['id']).first()
    # Business logic here?
    processor.requested_status = 'removed'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor remove requested.")


@proc.command(name='pause')
@click.option('-n', '--name', default=None, required=False)
@click.pass_context
def pause_processor(context, name):
    """
    Pause a processor
    """
    id = context.obj['id']

    if name is not None:
        print("Pausing ", name)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()
    elif id is not None:
        print("Pausing ", id)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    # Business logic here?
    processor.requested_status = 'paused'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor pause requested.")


@proc.command(name='resume')
@click.option('-n', '--name', default=None, required=False)
@click.pass_context
def resume_processor(context, name):
    """
    Pause a processor
    """
    id = context.obj['id']

    if name is not None:
        print("Pausing ", name)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()
    elif id is not None:
        print("Pausing ", id)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    # Business logic here?
    processor.requested_status = 'resumed'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor resume requested.")


@proc.command(name='stop')
@click.option('-n', '--name', default=None, required=False)
@click.pass_context
def stop_processor(context, name):
    """
    Stop a processor
    """
    id = context.obj['id']

    if name is not None:
        print("Stopping", name)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()
    elif id is not None:
        print("Stopping ", id)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    # Business logic here?
    processor.requested_status = 'stopped'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor stop requested.")


@proc.command(name='start')
@click.option('-n', '--name', default=None, required=False)
@click.pass_context
def start_processor(context, name):
    """
    Start a processor
    """
    id = context.obj['id']

    if name is not None:
        print("Starting", name)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()
    elif id is not None:
        print("Starting", id)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    # Business logic here?
    processor.requested_status = 'start'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor start requested.")


@proc.command(name='restart')
@click.option('-n', '--name', default=None, required=False)
@click.pass_context
def restart_processor(context, name):
    """
    Start a processor
    """
    id = context.obj['id']

    if name is not None:
        print("Restarting", name)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()
    elif id is not None:
        print("Restarting", id)
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    # Business logic here?
    processor.requested_status = 'restart'
    database = context.obj['database']
    database.session.add(processor)
    database.session.commit()
    print("Processor restart requested.")


@cli.group()
@click.option('--id', default=None, help="ID of processor")
@click.option('-n', '--name', default=None, required=False, help='Name of scheduler')
@click.pass_context
def scheduler(context, id, name):
    """
    Scheduler management commands
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj['id'] = str(id)
    context.obj['name'] = name


@cli.group(name="delete")
def delete():
    """
    Delete an object from the database
    """
    pass


@delete.command(name='socket', help="Delete a socket from the database")
@click.option('-n','--name', default=None, required=True, help="Name of socket being deleted")
@click.pass_context
def delete_socket(context, name):
    model = context.obj['database'].session.query(
        SocketModel).filter_by(name=name).first()

    context.obj['database'].session.delete(model)
    context.obj['database'].session.commit()


@delete.command(name='task', help="Delete a task from the database")
@click.option('-n','--name', default=None, required=True, help="Name of task being deleted")
@click.pass_context
def delete_task(context, name):
    model = context.obj['database'].session.query(
        TaskModel).filter_by(name=name).first()

    context.obj['database'].session.delete(model)
    context.obj['database'].session.commit()


@delete.command(name='processor', help="Delete a processor from the database")
@click.option('-n','--name', default=None, required=True, help="Name of processor being deleted")
@click.pass_context
def delete_processor(context, name):
    model = context.obj['database'].session.query(
        ProcessorModel).filter_by(name=name).first()

    context.obj['database'].session.delete(model)
    context.obj['database'].session.commit()


@delete.command(name='user', help="Delete a user object from the database")
@click.option('--id', default=None, required=True, help="ID of user being deleted")
@click.pass_context
def delete_user(context, id):
    model = context.obj['database'].session.query(
        UserModel).filter_by(id=id).first()

    context.obj['database'].session.delete(model)
    context.obj['database'].session.commit()


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
    Update a database object
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj['id'] = str(id)


@scheduler.command(name='start', help='Start the default scheduler')
@click.option('-n', '--name', default=None, required=True)
@click.option('-i', '--interval', default=3, required=False)
@click.pass_context
def start_scheduler(context, name, interval):
    from pyfi.scheduler import Scheduler
    print("Starting scheduler {} with interval {} seconds.".format(name, interval))
    scheduler = Scheduler(context, name, interval)
    scheduler.run()


@scheduler.command(name='add')
@click.option('-nd', '--node', default=None, required=False, help='Name of node to add')
@click.pass_context
def add_node_to_scheduler(context, node):
    """
    Add a node to a scheduler
    """
    id = context.obj['id']
    name = context.obj['name']

    if name is not None:
        scheduler = context.obj['database'].session.query(
            SchedulerModel).filter_by(name=name).first()

    elif id is not None:
        scheduler = context.obj['database'].session.query(
            SchedulerModel).filter_by(id=id).first()

    if scheduler is None:
        print(f"Scheduler {name} does not exist.")
        return

    _node = context.obj['database'].session.query(
        NodeModel).filter_by(name=node).first()

    if _node is None:
        print(f"Node {node} does not exist.")
        return

    scheduler.nodes += [_node]

    context.obj['database'].session.add(scheduler)
    context.obj['database'].session.commit()

    print('Node added.')


@cli.group()
def task():
    """
    Pyfi task management
    """
    pass



@task.command(name='show', help="Show details for a task")
@click.option('-n', '--name', required=True, help='Name of task to run')
@click.option('-g', '--gitrepo', is_flag=True, default=False)
@click.pass_context
def show_task(context, name, gitrepo):

    task = context.obj['database'].session.query(
        TaskModel).filter_by(name=name).first()

    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Module"]
    if gitrepo:
        names += ["Git Repo"]

    x.field_names = names
    
    nodes = [task]

    if task.code:
        print(task.code)

    for node in nodes:
        values = [node.name, node.id, node.owner,
                  node.lastupdated, node.module]
        if gitrepo:
            values += [node.gitrepo]

        x.add_row(values)

    print(x)

@task.command(name='run')
@click.option('-n', '--name', required=True, help='Name of task to run')
@click.option('-t', '--type', required=False, default='raw', help='Type of return data (json, pickle, raw)')
@click.option('-s', '--socket', required=True, help='Name of socket associated with the task to run')
@click.option('-d', '--data', required=False, help='String data to pass to the socket\'s task')
@click.pass_context
def run_task(context, name, type, socket, data):
    """
    Run a task
    """
    import sys
    import imp

    from pyfi.client.api import Socket

    if name:

        mymodule = imp.new_module(name)

        _task = context.obj['database'].session.query(
            TaskModel).filter_by(name=name).first()

        result = exec(_task.code, mymodule.__dict__)

        if result:
            print(result)
        return

    task = Socket(name=socket)

    if data:
        result = task(data)
    else:
        #
        # code = sys.stdin.read()
        # Determine mime type from code bytes
        # depickle or load json
        #
        lines = []
        for line in sys.stdin:
            stripped = line.strip()
            if not stripped: break
            lines.append(stripped)

        result = task(''.join(lines))

    # If type is set to pickle, then pickle the result
    # If type is set to json, then json dumps
    # otherwise type is 'raw', so print it
    print(result)


def update_object(obj, locals):
    """
    Docstring
    """
    for var in locals.keys():
        if locals[var] is not None and var != 'id':
            setattr(obj, var, locals[var])

    obj.updated = datetime.now()
    return obj


@update.command(name='processor')
@click.option('-n', '--name', default=None, required=False)
@click.option('-m', '--module', default=None, required=False)
@click.option('-h', '--hostname', default=None, help='Target server hostname')
@click.option('-w', '--workers', default=None, help='Number of worker tasks')
@click.option('-g', '--gitrepo', default=None, help='Git repo URI')
@click.option('-c', '--commit', default=None, help='Git commit id for processor code')
@click.option('-b', '--beat', default=None, is_flag=True, required=False)
@click.option('-r', '--requested_status', default=None, required=False)
@click.option('-br', '--branch', default=None, required=False)
@click.pass_context
def update_processor(context, name, module, hostname, workers, gitrepo, commit, beat, requested_status, branch):
    """
    Update a processor in the database
    """
    import inspect
    id = context.obj['id']

    if name is not None:
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()

    elif id is not None:
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    processor.requested_status = 'update'

    if not hostname:

        _hostname = click.prompt('Hostname',
                                 type=str, default=processor.hostname)
        if _hostname != processor.hostname:
            processor.requested_status = 'move'
            processor.hostname = _hostname

    if not module:
        processor.module = click.prompt('Module',
                                          type=str, default=processor.module)

    if not workers:
        processor.concurrency = click.prompt('Workers',
                                             type=int, default=processor.concurrency)

    if not gitrepo:
        processor.gitrepo = click.prompt('Gitrepo',
                                         type=str, default=processor.gitrepo)

    if not commit:
        processor.commit = click.prompt('Commit',
                                        type=str, default=processor.commit)

    if not branch:
        processor.commit = click.prompt('Branch',
                                        type=str, default=processor.branch)

    if not beat:
        processor.beat = click.prompt('Beat',
                                      type=bool, default=processor.beat)

    argspec = inspect.getargvalues(inspect.currentframe())
    _locals = argspec.locals
    processor = update_object(processor, _locals)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()


@add.command(name='task')
@click.option('-n', '--name', prompt=True, required=True, default=None, help="Name of this processor")
@click.option('-m', '--module', prompt=True, required=True, default=None, help="Python module (e.g. some.module.path")
@click.option('-c', '--code', is_flag=True, default=None, help='Code flag. reads from stdin.')
@click.pass_context
def add_task(context, name, module, code):
    """
    Add task to the database
    """

    if code:
        # get from stdin
        code = sys.stdin.read()


    task = TaskModel(name=name, module=module, code=code, gitrepo="None")
    task.updated = datetime.now()
    context.obj['database'].session.add(task)
    context.obj['database'].session.commit()
    print(task)


@add.command(name='processor')
@click.option('-n', '--name', prompt=True, required=True, default=None, help="Name of this processor")
@click.option('-m', '--module', prompt=True, required=True, default=None, help="Python module (e.g. some.module.path")
@click.option('-h', '--hostname', default=None, help='Target server hostname')
@click.option('-w', '--workers', default=1, help='Number of worker tasks')
@click.option('-r', '--retries', default=5, help='Number of retries to invoke this processor')
@click.option('-g', '--gitrepo', prompt=True, default=None, required=True, help='Git repo URI')
@click.option('-c', '--commit', default=None, help='Git commit id for processor code')
@click.option('-rs', '--requested_status', default='ready', required=False, help="The requested status for this processor")
@click.option('-b', '--beat', default=False, is_flag=True, required=False, help="Enable the beat scheduler")
@click.option('-br', '--branch', default='main', required=False, help="Git branch to be used for checkouts")
@click.pass_context
def add_processor(context, name, module, hostname, workers, retries, gitrepo, commit, requested_status, beat, branch):
    """
    Add processor to the database
    """
    id = context.obj['id']

    processor = ProcessorModel(
        id=id, status='ready', hostname=hostname, branch=branch, retries=retries, gitrepo=gitrepo, beat=beat, commit=commit, concurrency=workers, requested_status=requested_status, name=name, module=module)

    processor.updated = datetime.now()
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(processor)


@add.command(name='privilege')
@click.option('-u', '--user', prompt=True, default=None, required=True)
@click.option('-n', '--name', prompt=True, default=None, required=True)
@click.pass_context
def add_privilege(context, user, name):
    """
    Add privilege to the database
    """
    from sqlalchemy.exc import IntegrityError

    id = context.obj['id']
    try:
        user = context.obj['database'].session.query(
            UserModel).filter_by(name=user).first()
        user.lastupdated = datetime.now()
        privilege = PrivilegeModel(id=id, name=name, right=name)
        user.privileges += [privilege]
        context.obj['database'].session.add(privilege)
        context.obj['database'].session.add(user)
        context.obj['database'].session.commit()
        print("User added")
    except IntegrityError:
        import traceback
        print(traceback.format_exc())
        context.obj['database'].session.rollback()
        print("Error: Database constraint violation")


@add.command(name='user')
@click.option('-n', '--name', prompt=True, default=None, required=True)
@click.option('-e', '--email', prompt=True, default=None, required=True)
@click.option('-p', '--password', prompt=True, default=None, required=True)
@click.pass_context
def add_user(context, name, email, password):
    """
    Add user object to the database
    """
    from sqlalchemy.exc import IntegrityError
    from pyfi.db.model import Base

    id = context.obj['id']

    if name is None or email is None:
        raise click.UsageError("Name and Email are required")

    try:
        user = UserModel(name=name, password=password, email=email)
        user.lastupdated = datetime.now()

        context.obj['database'].session.add(user)
        context.obj['database'].session.commit()
        
        sql = f"CREATE USER {name} WITH PASSWORD '{password}'"
        print(sql)
        context.obj['database'].session.execute(sql)

        for t in Base.metadata.sorted_tables:
            sql = f"GRANT CONNECT ON DATABASE pyfi TO \"{name}\""
            context.obj['database'].session.execute(sql)
            sql = f"GRANT SELECT, UPDATE, INSERT, DELETE ON \"{t.name}\" TO \"{name}\""
            context.obj['database'].session.execute(sql)

        context.obj['database'].session.commit()
        print(f"User \"{name}\" added")
    except IntegrityError:
        import traceback
        print(traceback.format_exc())
        context.obj['database'].session.rollback()
        print("Error: Database constraint violation")


@add.command(name='scheduler')
@click.option('-n', '--name', required=True)
@click.option('-s', '--strategy', default='BALANCED', required=False)
@click.pass_context
def add_scheduler(context, name, strategy):
    """
    Add scheduler object to the database
    """
    id = context.obj['id']

    scheduler = SchedulerModel(name=name, strategy=strategy, id=id)
    scheduler.updated = datetime.now()
    context.obj['database'].session.add(scheduler)
    context.obj['database'].session.commit()
    print(scheduler)


@add.command(name='node')
@click.option('-n', '--name', required=True)
@click.option('-h', '--hostname', default=None, help='Hostname of the node')
@click.pass_context
def add_node(context, name, hostname):
    """
    Add node object to the database
    """
    id = context.obj['id']

    node = NodeModel(name=name, id=id, hostname=hostname)
    node.updated = datetime.now()
    context.obj['database'].session.add(node)
    context.obj['database'].session.commit()
    print(node)


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
@click.option('-n', '--name', required=True)
@click.option('-t', '--type', type=click.Choice(['topic', 'direct', 'fanout'], case_sensitive=False), show_default=True, default='direct', required=True)
@click.pass_context
def add_queue(context, name, type):
    """
    Add queue object to the database
    """
    id = context.obj['id']

    queue = QueueModel(name=name, id=id, qtype=type, requested_status='create',
                       status='ready')

    queue.updated = datetime.now()
    context.obj['database'].session.add(queue)
    context.obj['database'].session.commit()
    print(queue)


@update.command(name='socket')
@click.option('-n', '--name', required=True)
@click.option('-q', '--queue', required=True, help="Queue name")
@click.option('-i', '--interval', default=None, required=False)
@click.option('-pi', '--procid', default=None, required=False, help="Processor id")
@click.option('-pn', '--procname', default=None, required=False, help="Processor name")
@click.option('-t', '--task', default=None, required=False, help="Task name")
@click.pass_context
def update_socket(context, name, queue, interval, procid, procname, task):
    """
    Update a socket in the database
    """
    import inspect
    id = context.obj['id']

    # Get the named or id of the plug model
    if name is not None:
        socket = context.obj['database'].session.query(
            SocketModel).filter_by(name=name).first()
    elif id is not None:
        socket = context.obj['database'].session.query(
            SocketModel).filter_by(id=id).first()

    if not interval:
        socket.interval = click.prompt('Interval',
                                       type=int, default=socket.interval)
    return


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
        plug = context.obj['database'].session.query(
            PlugModel).filter_by(name=name).first()
    elif id is not None:
        plug = context.obj['database'].session.query(
            PlugModel).filter_by(id=id).first()

    # Get the plug's current processor
    current_processor = context.obj['database'].session.query(
        ProcessorModel).filter_by(id=plug.processor_id).first()

    # Get the processor referenced in the CLI
    if procname is not None:
        new_processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=procname).first()
    elif procid is not None:
        new_processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=procid).first()

    # If the new processor is different, then add it to the transaction
    # and request it be updated by the agent
    if new_processor.id != current_processor.id:
        new_processor.requested_status = 'update'
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
    current_processor.requested_status = 'update'
    context.obj['database'].session.add(plug)
    context.obj['database'].session.add(current_processor)
    context.obj['database'].session.commit()
    print(plug)


@add.command(name='plug')
@click.option('-n', '--name', required=True)
@click.option('-q', '--queue', required=True, help="Queue name")
@click.option('-si', '--socketid', default=None, required=False, help="Socket id")
@click.option('-sn', '--socketname', default=None, required=False, help="Socket name")
@click.option('-pi', '--procid', default=None, required=False, help="Processor id")
@click.option('-pn', '--procname', default=None, required=False, help="Processor name")
@click.pass_context
def add_plug(context, name, queue, socketid, socketname, procid, procname):
    """
    Add plug to a processor
    """
    id = context.obj['id']

    if socketname is not None:
        socket = context.obj['database'].session.query(
            SocketModel).filter_by(name=socketname).first()
    elif socketid is not None:
        socket = context.obj['database'].session.query(
            SocketModel).filter_by(id=socketid).first()

    if procname is not None:
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=procname).first()
    elif procid is not None:
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=procid).first()

    queue = context.obj['database'].session.query(
        QueueModel).filter_by(name=queue).first()
    plug = PlugModel(name=name, id=id, requested_status='create',
                     status='ready', processor_id=procid)
    plug.socket = socket
    plug.queue = queue
    plug.updated = datetime.now()
    processor.plugs += [plug]

    context.obj['database'].session.add(plug)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(plug)


@add.command(name='socket')
@click.option('-n', '--name', required=True)
@click.option('-q', '--queue', required=True, help="Queue name")
@click.option('-i', '--interval', default=10, required=False, help="Interval in seconds this socket is triggered")
@click.option('-pn', '--procname', default=None, required=True, help="Processor name")
@click.option('-t', '--task', default=None, required=True, help="Task name")
@click.pass_context
def add_socket(context, name, queue, interval, beat, procname, task):
    """
    Add socket to a processor
    """
    id = context.obj['id']

    processor = context.obj['database'].session.query(
        ProcessorModel).filter_by(name=procname).first()

    queue = context.obj['database'].session.query(
        QueueModel).filter_by(name=queue).first()
    socket = SocketModel(name=name, id=id, requested_status='create',
                         status='ready', processor_id=processor.id)

    if task is not None:
        _task = context.obj['database'].session.query(
            TaskModel).filter_by(name=task).first()
        if _task is None:
            _task = TaskModel(name=task)
            context.obj['database'].session.add(_task)
        socket.task = _task

    socket.queue = queue
    socket.interval = interval
    socket.updated = datetime.now()
    processor.sockets += [socket]
    processor.requested_status = 'update'
    context.obj['database'].session.add(socket)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()
    print(socket)


@cli.group()
def ls():
    """
    List database objects and their relations
    """
    pass


@cli.group()
def worker():
    """
    Run pyfi worker
    """
    pass


@cli.group()
def agent():
    """
    Run pyfi agent
    """
    pass


@worker.command(name='start', help='Start a pyfi worker')
@click.option('-n', '--name', required=True, help="Name of worker")
@click.option('-p', '--pool', default=4, required=False, help="Size of worker pool")
@click.option('-s', '--skip-venv', is_flag=True, default=False, required=False, help="Skip building the virtual environment")
@click.pass_context
def start_worker(context, name, pool, skip_venv):
    from pyfi.worker import Worker

    workerModel = context.obj['database'].session.query(
        WorkerModel).filter_by(name=name).first()

    worker = {}
    processor = context.obj['database'].session.query(ProcessorModel).filter_by(id=workerModel.processor_id).first()

    dir = 'work/'+processor.id
    os.makedirs(dir, exist_ok=True)

    workerproc = Worker(
        processor, workdir=dir, pool=pool, database=context.obj['dburi'], skipvenv=skip_venv, celeryconfig=None, backend=CONFIG.get('backend', 'uri'), broker=CONFIG.get('broker', 'uri'))

    wprocess = workerproc.start()

    processor.worker.requested_status = 'ready'
    processor.worker.status = 'running'
    context.obj['database'].session.add(
        processor.worker)

    context.obj['database'].session.commit()
    wprocess.join()


@ls.command(name='call')
@click.option('--id', default=None, help="ID of call")
@click.option('-n', '--name', default=None, required=False, help='Name of call')
@click.option('-r', '--result', default=False, is_flag=True, help="Include result of call")
@click.option('-t', '--tree', default=False, is_flag=True, help="Show forward call tree")
@click.option('-g', '--graph', default=False, is_flag=True, help="Show complete call graph")
@click.option('-f', '--flow', default=False, is_flag=True, help="Show all calls in a workflow")
@click.pass_context
def ls_call(context, id, name, result, tree, graph, flow):
    """
    List details about a call record
    """
    import redis
    import json

    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Socket", "Started", "Finished", "State"]
    x.field_names = names
    
    calls = None
    call = None

    if name is not None:
        calls = context.obj['database'].session.query(
            CallModel).filter_by(name=name).all()
    elif id is not None:
        call = context.obj['database'].session.query(
            CallModel).filter_by(id=id).first()

        if flow:
            nodes = context.obj['database'].session.query(
                CallModel).filter_by(task_id=call.task_id).all()
        else:
            nodes = [call]

    if calls:
        nodes = calls
    elif call:
        import pickle
        
        if result:
            redisclient = redis.Redis.from_url(CONFIG.get('backend', 'uri'))
            r = redisclient.get(call.resultid)

            _r = pickle.loads(r)
            print(json.dumps(_r, indent=4))
            return

        if graph:
            calls = context.obj['database'].session.query(
                CallModel).filter_by(task_id=call.task_id).all()

            calldict = {}

            for call in calls:
                calldict[call.celeryid] = call

            from pptree import print_tree, Node

            for call in calls:
                if call.taskparent is None:
                    root = Node(call.name)
                    break

            def get_call_graph(parent, node, _calls):

                for _child in _calls:
                    if _child.taskparent == node.celeryid:
                        _child_node = Node(_child.name, parent)
                        _child_node = get_call_graph(_child_node, _child, _calls)

                return parent

            root = get_call_graph(root, call, calls)

            print_tree(root, horizontal=False)
            if not tree:
                return
        if tree:
            from pptree import print_tree, Node
            
            root = Node(call.name)

            def get_call_graph(root, _call):
                _calls = context.obj['database'].session.query(
                    CallModel).filter_by(parent=_call.id).all()

                for _child in _calls:
                    _child_node = Node(_child.name, root)
                    _child_node = get_call_graph(_child_node, _child)

                return root

            root = get_call_graph(root, call)
            print_tree(root, horizontal=False)
            return

    for node in nodes:
        x.add_row([node.name, node.id, node.owner,
                    node.lastupdated, node.socket.name, node.started, node.finished, node.state])
    print(x)
    x = PrettyTable()
    print("Provenance")
    names = ["Task", "Task Parent", "Flow Parent"]
    x.field_names = names
    x.add_row([ node.celeryid, node.taskparent, node.parent])
    print(x)
    x = PrettyTable()
    print('Events')
    names = ["Name", "ID", "Owner", "Last Updated", "Note"]
    x.field_names = names
    if call:
        for event in call.events:
            x.add_row([event.name, event.id, event.owner,
                    event.lastupdated, event.note])
    print(x)


@ls.command(name='calls')
@click.option('-p', '--page', default=1, required=False)
@click.option('-r', '--rows', default=10, required=False)
@click.option('-a', '--ascend', default=False, is_flag=True, required=False)
@click.pass_context
def ls_calls(context, page, rows, ascend):
    """
    List queues
    """
    x = PrettyTable()

    names = ["Page","Row", "Name", "ID", "Owner", "Last Updated", "Socket", "Started", "Finished", "State"]
    x.field_names = names

    total = context.obj['database'].session.query(CallModel).count()
    if page > round(total/rows):
        print("Only {} pages exist.".format(round(total/rows)))
        return

    if not ascend:
        if total < rows:
            nodes = context.obj['database'].session.query(
                CallModel).all()
        else:
            nodes = context.obj['database'].session.query(
                CallModel).order_by(CallModel.lastupdated.desc()).offset((page-1)*rows).limit(rows)
    else:
        if total < rows:
            nodes = context.obj['database'].session.query(
                CallModel).all()
        else:
            nodes = context.obj['database'].session.query(
                CallModel).order_by(CallModel.lastupdated.asc()).offset((page-1)*rows).limit(rows)

    row = 0
    for node in nodes:
        row += 1
        x.add_row([page, row, node.name, node.id, node.owner,
                  node.lastupdated, node.socket.name,  node.started, node.finished, node.state])

    print(x)

    if total > 0:
        print("Page {} of {} of {} total records".format(
            page, round(total/rows), total))
    else:
        print("No rows")


@ls.command(name='schedulers')
@click.pass_context
def ls_schedulers(context):
    """
    List queues
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Strategy", "Nodes"]
    x.field_names = names
    nodes = context.obj['database'].session.query(SchedulerModel).all()
    for node in nodes:
        x.add_row([node.name, node.id, node.owner,
                  node.lastupdated, node.strategy, [n.name for n in node.nodes]])

    print(x)


@ls.command(name='nodes')
@click.pass_context
def ls_nodes(context):
    """
    List queues
    """
    import humanize

    x = PrettyTable()

    names = ["Name", "ID", "Host", "Owner", "Last Updated", "CPUs", "Mem Size", "Free Mem", "Used Mem", "Agent"]
    x.field_names = names
    nodes = context.obj['database'].session.query(NodeModel).all()
    for node in nodes:
        x.add_row([node.name, node.id, node.hostname,
                  node.owner, node.lastupdated, node.cpus, humanize.naturalsize(node.memsize, gnu=True), humanize.naturalsize(node.freemem, gnu=True), humanize.naturalsize(node.memused, gnu=True), node.agent.name])

    print(x)


@ls.command(name='queues')
@click.pass_context
def ls_queues(context):
    """
    List queues
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Message TTL", "Expires",
             "Requested Status", "Status", "Type"]
    x.field_names = names
    queues = context.obj['database'].session.query(QueueModel).all()
    for node in queues:
        x.add_row([node.name, node.id, node.owner, node.lastupdated, node.message_ttl, node.expires,
                  node.requested_status, node.status, node.qtype])

    print(x)


@ls.command(name='users')
@click.pass_context
def ls_users(context):
    """
    List users
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Email"]
    x.field_names = names
    users = context.obj['database'].session.query(UserModel).all()
    for user in users:
        x.add_row([user.name, user.id, user.owner, user.email])

    print(x)


@ls.command(name='user')
@click.option('-n', '--name', default=None, required=True)
@click.pass_context
def ls_user(context, name):
    """
    List users
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Email"]
    x.field_names = names
    user = context.obj['database'].session.query(UserModel).filter_by(name=name).first()
    x.add_row([user.name, user.id, user.owner, user.email])

    print(x)

    x = PrettyTable()
    print("Privileges")
    names = ["Name", "Right", "Last Updated", "By"]
    x.field_names = names

    for priv in user.privileges:
        x.add_row([user.name, priv.right, priv.lastupdated, priv.owner])

    print(x)


@ls.command(name='workers')
@click.pass_context
def ls_workers(context):
    """
    List workers
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated",
             "Requested Status", "Status", "Backend", "Broker", "Hostname", "Processor"]
    x.field_names = names
    workers = context.obj['database'].session.query(WorkerModel).all()

    for node in workers:
        x.add_row([node.name, node.id, node.owner, node.lastupdated,
                  node.requested_status, node.status, node.backend, node. broker, node.hostname, node.processor.name])

    print(x)


@ls.command(name='processors')
@click.option('-g', '--gitrepo', is_flag=True, default=False)
@click.option('-m', '--module', is_flag=True, default=False)
@click.option('-t', '--task', is_flag=True, default=False)
@click.option('-o', '--owner', is_flag=True, default=False)
@click.pass_context
def ls_processors(context, gitrepo, module, task, owner):
    """
    List processors
    """
    processors = context.obj['database'].session.query(ProcessorModel).all()
    x = PrettyTable()

    names = ["Name", "Worker", "ID", "Module", "Host", "Owner", "Last Updated",
             "Requested Status", "Status", "Concurrency", "Beat"]

    if gitrepo:
        names += ["Git"]
    if module:
        names += ["Module"]
    if task:
        names += ["Task"]
    if owner:
        names += ["Owner"]

    x.field_names = names

    for processor in processors:
        workername = processor.worker.name if processor.worker else "None"
        row = [processor.name, workername, processor.id, processor.module, processor.hostname, processor.owner, processor.lastupdated,
               processor.requested_status, processor.status, processor.concurrency, processor.beat]

        if gitrepo:
            row += [processor.gitrepo]
        if module:
            row += [processor.module]
        if task:
            row += [processor.task]
        if owner:
            row += [processor.owner]

        x.add_row(row)

    print(x)


@ls.command(name='tasks')
@click.option('-g', '--gitrepo', is_flag=True, default=False)
@click.pass_context
def ls_tasks(context, gitrepo):
    """
    List agents
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Module"]
    if gitrepo:
        names += ["Git Repo"]
    x.field_names = names
    tasks = context.obj['database'].session.query(TaskModel).all()

    for node in tasks:
        values = [node.name, node.id, node.owner, node.lastupdated, node.module]
        
        if gitrepo:
            values += [node.gitrepo]
        x.add_row(values)

    print(x)


@ls.command(name='agent')
@click.pass_context
def ls_agent(context):
    """
    List an agent
    """
    pass



@ls.command(name='agents')
@click.pass_context
def ls_agents(context):
    """
    List agents
    """
    import requests

    x = PrettyTable()

    names = ["Name", "ID", "Host", "Port", "Owner", "Last Updated",
             "Status", "Node", "Worker"]
    x.field_names = names
    agents = context.obj['database'].session.query(AgentModel).all()

    for node in agents:
        worker_name = node.worker.name if node.worker else 'None'
        status = 'unreachable'
        try:
            res = requests.get('http://'+node.hostname+':'+str(node.port))
            if res.status_code == 200:
                status = 'running'
        except:
            pass
        x.add_row([node.name, node.id, node.hostname, node.port, node.owner, node.lastupdated,
                  status, node.node.name, worker_name])

    print(x)


@ls.command(name='sockets')
@click.pass_context
def ls_sockets(context):
    """
    List sockets
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Module", "Task", "Last Updated",
             "Status", "Processor", "Queue", "Interval"]
    x.field_names = names
    sockets = context.obj['database'].session.query(SocketModel).all()

    for node in sockets:
        x.add_row([node.name, node.id, node.owner, node.task.module, node.task.name, node.lastupdated,
                  node.status, node.processor.name, node.queue.name, node.interval])

    print(x)


@ls.command(name='node')
@click.option('-n', '--name', default=None, required=True, help="Name of node")
@click.option('-t', '--tree', default=False, is_flag=True, required=False, help="Display object tree")
@click.option('-h', '--horizontal', default=True, is_flag=True, required=False, help="Vertical tree mode")
@click.pass_context
def ls_node(context, name, tree, horizontal):
    """
    List a node
    """
    from pptree import print_tree, Node

    node = context.obj['database'].session.query(
        NodeModel).filter_by(name=name).first()

    if not node:
        return

    if tree:
        root = Node("node::"+node.name)
        agent = Node("agent::"+node.agent.name, root)
        worker = Node("worker::"+node.agent.worker.name, agent)
        processor = Node(
            "processor::"+node.agent.worker.processor.name, worker)

        for socket in node.agent.worker.processor.sockets:
            _sock = Node("socket::"+socket.name, processor)
            Node("task::"+socket.task.name, _sock)

        print_tree(root, horizontal=not horizontal)
    
@ls.command(name='plug')
@click.option('-n', '--name', default=None, required=True, help="Name of processor")
@click.pass_context
def ls_plug(context, name):
    """
    List a plug
    """
    x = PrettyTable()

    plug = context.obj['database'].session.query(
        PlugModel).filter_by(name=name).first()

    names = ["Name", "ID", "Owner", "Last Updated",
             "Status", "Queue", "Source Task", "Target Task","Source Socket", "Target Socket"]
    x.field_names = names

    node = plug
    x.add_row([node.name, node.id, node.owner, node.lastupdated,
                node.status, node.queue.name, node.source.task.name, node.target.task.name, node.source.name, node.target.name])

    print(x)

@ls.command(name='plugs')
@click.pass_context
def ls_plugs(context):
    """
    List agents
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated",
             "Status", "Processor", "Queue", "Source", "Target"]
    x.field_names = names
    plugs = context.obj['database'].session.query(PlugModel).all()

    for node in plugs:
        x.add_row([node.name, node.id, node.owner, node.lastupdated,
                  node.status, node.processor.name, node.queue.name, node.source.name, node.target.name])

    print(x)


@cli.command(help="Listen to a processor output")
@click.option('-n', '--name', default=None, required=True, help="Name of processor")
@click.option('-c', '--channel', default='task', required=True, help="Listen channel (e.g. task, log, etc)")
@click.option('-a', '--adaptor', default=None, help="Adaptor class function (e.g. my.module.class.function)")
@click.pass_context
def listen(context, name, channel, adaptor):
    """
    Listen on a pub/sub channel
    """
    import redis
    import importlib

    redisclient = redis.Redis.from_url(CONFIG.get('backend', 'uri'))
    p = redisclient.pubsub()
    p.psubscribe([name+'.'+channel])
    print("Listening to",name)
    func = None
    if adaptor:
        module = importlib.import_module('.'.join(adaptor.rsplit('.')[:-1]))
        _class = getattr(module, adaptor.rsplit('.')[-1:][0])
        print("Loaded adaptor function",adaptor)
        func = _class()

    while True:
        for item in p.listen():
            print(item)
            if func:
                func.put(item)


@cli.command(help="Database login user")
@click.pass_context
def whoami(context):
    """
    Print who I am logged in as
    """
    print("I am", context.obj['owner'])

@cli.group()
def api():
    """
    API server admin
    """
    pass


@api.command(name='start')
@click.option('-ip', default=HOSTNAME, help='IP bind address')
@click.option('-p', '--port', default=8000, help='Listen port')
@click.pass_context
def api_start(context, ip, port):
    """
    Run pyfi API server
    """
    import bjoern
    from pyfi.server import app as server
    logging.info("Initializing server app....")
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
@click.option('-p', '--port', default=8002, help='Listen port')
@click.option('--clean', default=False, is_flag=True, help="Remove work directories before launch")
@click.option('-b', '--backend', default='redis://localhost', help='Message backend URI')
@click.option('-r', '--broker', default='pyamqp://localhost', help='Message broker URI')
@click.option('-c', '--config', default=None, help='Config module.object import (e.g. path.to.module.MyConfigClass')
@click.option('-q', '--queues', is_flag=True, help='Run the queue monitor only')
@click.option('-u', '--user', default=None, help='Run the worker as user')
@click.option('-p', '--pool', default=4, help='Process pool for message dispatches')
@click.pass_context
def start_agent(context, port, clean, backend, broker, config, queues, user, pool):
    """
    Run pyfi agent server
    """
    from pyfi.agent import Agent

    agent = Agent(context.obj['database'], context.obj['dburi'], port, pool=pool,
                  config=config, backend=backend, user=user, clean=clean, broker=broker)
    agent.start()


@cli.group()
@click.pass_context
def web(context):
    """
    Web server admin
    """
    pass


@web.command(name='start')
@click.option('-p', '--port', default=8001, help='Listen port')
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
