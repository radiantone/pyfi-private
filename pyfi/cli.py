"""
cli.py - pyfi CLI command tool for managing database
"""
from sqlalchemy import exc as sa_exc
import os
import sys
import logging
import getpass
import platform
import configparser
import hashlib

import click
from pyfi.server import app

from pathlib import Path
from datetime import datetime

from flask import Flask

import pyfi.db.postgres

from sqlalchemy import create_engine, MetaData, literal_column
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

from pyfi.db.model.models import PrivilegeModel
from pyfi.db.model import oso, SchedulerModel, UserModel, EventModel, LoginModel, AgentModel, WorkerModel, CallModel, PlugModel, SocketModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel
from pyfi.web import run_http
from sqlalchemy_oso import authorized_sessionmaker

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
@click.option('-a', '--api', help='Message broker API URI')
@click.option('-u', '--user', help='Message broker API user')
@click.option('-p', '--password', help='Message broker API password')
@click.option('-i', '--ini', default=home+"/pyfi.ini", help='PYFI .ini configuration file')
@click.option('-c', '--config', default=False, is_flag=True, help='Configure pyfi')
@click.pass_context
def cli(context, debug, db, backend, broker, api, user, password, ini, config):
    """
    PYFI CLI for creating & managing PYFI networks
    """
    from urllib.parse import urlparse

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    if debug:
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    context.obj = {}
    # If login section, then query for User and see if token matches and still valid

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
        if not api:
            api = click.prompt('Message broker API',
                               type=str, default='http://localhost:15672/api')
        if not user:
            user = click.prompt('Message broker API username',
                                type=str, default='guest')
        if not password:
            password = click.prompt('Message broker API password',
                                    type=str, default='guest')

        email = click.prompt('Postgres user email', type=str, default='p@e')
        password = click.prompt('Postgres user password',
                                type=str, default='pyfi101')

        _password = hashlib.md5(password.encode()).hexdigest()

        _config = configparser.ConfigParser()

        _config.add_section('login')

        _config.set('login', 'password', _password)
        _config.set('login', 'user', 'postgres')

        _config.add_section('database')
        _config.set('database', 'uri', db)

        _config.add_section('backend')
        _config.set('backend', 'uri', backend)

        _config.add_section('broker')
        _config.set('broker', 'uri', broker)
        _config.set('broker', 'api', api)
        _config.set('broker', 'user', user)
        _config.set('broker', 'password', password)

        with open(home+"/pyfi.ini", "w") as configfile:
            _config.write(configfile)

        print("Configuration file created at {}".format(home+"/pyfi.ini"))

    if not os.path.exists(ini) and db is None:
        print("No database uri configured. Please run \033[1m $ pyfi --config")
        exit(1)

    # If there is a user login in pyfi.ini then construct the DB URI
    # using their login info

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
        # print(traceback.format_exc())
        print("Database unavailable. Please check your configuration or ensure database server is running.")
        return

    if CONFIG.has_section('login'):
        username = CONFIG.get('login', 'user')
        password = CONFIG.get('login', 'password')

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            try:
                #engine = create_engine(db)
                #engine.uri = db
                session = sessionmaker(bind=engine)()

                user_m = session.query(
                    UserModel).filter_by(name=username, password=password).first()
                #context.obj['user'] = user_m
                # context.obj['database'].session.add(user_m)
                if username is None:
                    return

                if user_m is None:
                    print(f"Unable to log in {username}.")
                    return

                logging.debug(f"{user_m.name} logged in.")

                session.expunge(user_m)
            except:
                context.obj['user'] = None
                print(f"Unable to log in {username}..")
                return

            finally:
                session.close()

        oso.load_files([home+"/pyfi.polar"])

        context.obj['database'].session.close()

        def get_checked_permissions(*args, **kwargs):
            logging.debug("cli: get_checked_permissions")

            #engine = create_engine(db)
            #engine.uri = db
            session = sessionmaker(bind=engine)()
            _user = session.query(
                UserModel).filter_by(name=username, password=password).first()
            permissions = {PrivilegeModel: "read", AgentModel: "read",
                           NodeModel: "read", EventModel: "read", CallModel: "read", TaskModel: "read", QueueModel: "read", SocketModel: "read", PlugModel: "read", WorkerModel: "read", UserModel: "read", ProcessorModel: "read", RoleModel: "read"}

            for privilege in _user.privileges:
                if privilege.right == 'READ_LOG':
                    permissions[LogModel] = "read"

            session.close()

            return permissions

        from functools import partial

        user_object = None

        context.obj['session'] = session = authorized_sessionmaker(get_oso=lambda: oso,
                                                                   get_user=lambda: user_m,
                                                                   get_checked_permissions=get_checked_permissions,
                                                                   bind=engine)()
        user_m2 = user_object = session.query(
            UserModel).filter_by(name=username, password=password).first()
        # Add the logged in user to the authorized_session
        # context.obj['database'].session.merge(user_m)
        session.add(user_m2)
        context.obj['user'] = user_m2
        context.obj['database'].session = session  # context.obj['session']
        # Load the base policy file into OSO

        # Generate OSO user policy file based on roles and privileges in the database
        # Then load the policy file into oso

        # Update database URI based on logged in user
    else:
        context.obj['user'] = None

    if len(sys.argv) == 1:
        click.echo(context.get_help())


@cli.group()
def user():
    """
    User commands
    """
    pass


@user.command(name="remove")
@click.option('-u', '--user', default=None, required=True)
@click.option('-r', '--role', default=None, required=False)
@click.option('-p', '--privilege', default=None, required=False)
@click.pass_context
def user_remove(context, user, role, privilege):
    """
    Remove roles and privileges from a user
    """
    return


@user.command(name="add")
@click.option('-u', '--user', default=None, required=True)
@click.option('-r', '--role', default=None, required=False)
@click.option('-p', '--privilege', default=None, required=False)
@click.pass_context
def user_add(context, user, role, privilege):
    """
    Add roles and privileges to a user
    """
    user_m = context.obj['database'].session.query(
        UserModel).filter_by(name=user).first()
    if role:
        role_m = context.obj['database'].session.query(
            RoleModel).filter_by(name=role).first()
        print("ROLE:", role_m)
        user_m.roles += [role_m]
        database = context.obj['database']
        database.session.add(user_m)
        database.session.add(role_m)
        database.session.commit()
        print("Role {} added to {}.".format(role_m.name, user_m.name))
    elif privilege:
        pass
    else:
        print("Nothing to do.")


@cli.group()
def compose():
    """ Manage declarative infrastructure files """


@compose.command(name='kill')
@click.argument('filename')
@click.pass_context
def compose_kill(context, filename):
    """ Kill a running infrastructure """
    import yaml
    from pyfi.yaml.builder import stop_network

    with open(filename, "r") as stream:
        try:
            detail = yaml.safe_load(stream)
            stop_network(detail)
        except yaml.YAMLError as exc:
            print(exc)


@compose.command(name='build')
@click.argument('filename')
@click.pass_context
def compose_build(context, filename):
    """ Build infrastructure from a yaml file"""
    import yaml
    from pyfi.yaml.builder import build_network

    with open(filename, "r") as stream:
        try:
            detail = yaml.safe_load(stream)
            build_network(detail)
        except yaml.YAMLError as exc:
            print(exc)


@cli.command()
def logout():
    """ Logout current user """
    ini = home+"/pyfi.ini"

    if CONFIG.has_option('login', 'user'):
        CONFIG.remove_section('login')
        print("Logged out.")

    with open(ini, 'w') as inifile:
        CONFIG.write(inifile)


@cli.command()
@click.pass_context
@click.option('-d', '--database', is_flag=True, default=False, help="Database login only")
def login(context, database):
    """
    Log into PYFI CLI
    """
    import hashlib
    from urllib.parse import urlparse

    ini = home+"/pyfi.ini"

    user = None

    if context.obj['user'] is not None:
        print("Please logout first.")
        return

    if CONFIG.has_option('login', 'user'):
        _user = CONFIG.get('login', 'user')
    else:
        CONFIG.add_section('login')

    password = None
    if CONFIG.has_option('login', 'password'):
        _password = CONFIG.get('login', 'password')

    user = click.prompt('User',
                        type=str)
    __password = click.prompt('Password',
                              type=str)
    password = hashlib.md5(__password.encode()).hexdigest()

    CONFIG.set('login', 'user', user)

    if not database:
        user_m = context.obj['database'].session.query(
            UserModel).filter_by(name=user, password=password).first()

        if user_m is not None:
            _login = LoginModel(user=user_m)
            context.obj['database'].session.add(_login)
            context.obj['database'].session.commit()
            print("Logged in.")
        else:
            print("Invalid login.")

    dburi = CONFIG.get('database', 'uri')
    uri = urlparse(dburi)
    newuri = uri.scheme+'://'+user+':'+__password + \
        '@'+uri.hostname+':'+str(uri.port)+uri.path
    CONFIG.set('database', 'uri', newuri)
    CONFIG.set('login', 'password', password)

    with open(ini, 'w') as inifile:
        CONFIG.write(inifile)


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

        if CONFIG.has_section('login'):
            CONFIG.remove_section('login')

        dropdb(context)
        context.invoke(db_init)


def dropdb(context):
    from pyfi.db.model import Base

    # For every user in "user" table, DROP USER name

    _users = [u.name for u in context.obj['database'].session.query(
        UserModel).all()]

    for user in _users:
        if user != 'postgres':
            context.obj['database'].session.execute(
                f"DROP OWNED BY {user}")
            context.obj['database'].session.execute(
                f"DROP USER {user}")
            print("Dropped user {}".format(user))

    context.obj['database'].session.commit()

    for t in Base.metadata.sorted_tables:
        try:
            print("Dropping {}".format(t.name))
            t.drop(context.obj['database'])
            print("Dropped {}".format(t.name))
        except:
            import traceback
            print(traceback.format_exc())

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
    # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html
    meta.reflect(bind=engine)
    result = {}
    for table in meta.sorted_tables:
        result[table.name] = [dict(row)
                              for row in engine.execute(table.select())]
    print(json.dumps(result, indent=4, default=str))


@db.command(name='init')
@click.option('-r', '--rls', is_flag=True, default=False, help="Row level security")
def db_init(rls):
    """
    Initialize database tables
    """
    import hashlib

    ini = home+"/pyfi.ini"

    try:
        from sqlalchemy import create_engine

        try:
            _engine = create_engine(CONFIG.get('database', 'uri'))
            _session = sessionmaker(bind=_engine)()
            users = _session.query(UserModel).all()
            print("Database already created. Please run \"pyfi db drop\".")
            _session.close()
            return
        except:
            pass

        try:
            engine = create_engine(POSTGRES_ROOT+'postgres')
            session = sessionmaker(bind=engine)()

            session.connection().connection.set_isolation_level(0)
            session.execute('CREATE DATABASE pyfi')
            session.connection().connection.set_isolation_level(1)
            print("Database created")
            session.close()
        except:
            pass

        try:
            engine = create_engine(CONFIG.get('database', 'uri'))
            engine.uri = db
            session = sessionmaker(bind=engine)()
            session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            session.commit()
            #context.obj['database'] = engine
            #context.obj['session'] = session
            engine.session = session
        except:
            pass

        from pyfi.db.model import Base

        Base.metadata.create_all(engine)
        session.commit()

        try:
            sql = "ALTER TABLE \"user\" ENABLE ROW LEVEL SECURITY"
            print("Enabling security on table user")
            session.execute(sql)
            session.commit()
            sql = "CREATE POLICY user_security ON \"user\" USING (user.owner::text = current_user)"
            session.execute(sql)
            session.commit()
        except:
            pass

        try:
            sql = "ALTER TABLE \"login\" ENABLE ROW LEVEL SECURITY"
            print("Enabling security on table login")
            session.execute(sql)
            session.commit()
            sql = "CREATE POLICY user_security ON \"login\" USING (login.owner::text = current_user)"
            session.execute(sql)
            session.commit()
        except:
            pass

        session = sessionmaker(bind=engine)()

        if rls:
            for t in Base.metadata.sorted_tables:
                try:
                    sql = f"ALTER TABLE \"{t.name}\" ENABLE ROW LEVEL SECURITY"
                    print("Enabling security on table {}".format(t.name))
                    session.execute(sql)
                    session.commit()
                except Exception as ex:
                    print(ex)
                    session.rollback()

                try:
                    sql = f"CREATE POLICY {t.name}_security ON \"{t.name}\" USING ({t.name}.owner::text = current_user)"
                    print(sql)
                    session.execute(sql)
                    session.commit()
                except Exception as ex:
                    print(ex)
                    session.rollback()

        print("Database create all schemas done.")

        email = click.prompt('Postgres user email', type=str, default='p@e')
        password = click.prompt('Postgres user password', type=str, default='pyfi101')

        _password = hashlib.md5(password.encode()).hexdigest()

        if not CONFIG.has_section('login'):
            CONFIG.add_section('login')

        CONFIG.set('login', 'password', _password)
        CONFIG.set('login', 'user', 'postgres')

        with open(ini, 'w') as inifile:
            CONFIG.write(inifile)

        user = UserModel(name='postgres', email=email,
                         password=_password, clear=password)
        role = RoleModel(name='admin')
        user.roles += [role]
        session.add(role)
        session.add(user)
        session.commit()
        session.close()
        print("Updated postgres user.")

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


@delete.command(name='calls', help="Delete all the call records")
@click.pass_context
def delete_calls(context):
    rows = context.obj['database'].session.query(
        CallModel).delete()
    print(rows, "deleted.")


@delete.command(name='socket', help="Delete a socket from the database")
@click.option('-n', '--name', default=None, required=True, help="Name of socket being deleted")
@click.pass_context
def delete_socket(context, name):
    model = context.obj['database'].session.query(
        SocketModel).filter_by(name=name).first()

    context.obj['database'].session.delete(model)
    context.obj['database'].session.commit()


@delete.command(name='task', help="Delete a task from the database")
@click.option('-n', '--name', default=None, required=True, help="Name of task being deleted")
@click.pass_context
def delete_task(context, name):
    model = context.obj['database'].session.query(
        TaskModel).filter_by(name=name).first()

    context.obj['database'].session.delete(model)
    context.obj['database'].session.commit()


@delete.command(name='processor', help="Delete a processor from the database")
@click.option('-n', '--name', default=None, required=True, help="Name of processor being deleted")
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
@click.option('-n', '--name', required=False, help='Name of task to run')
@click.option('-t', '--type', required=False, default='raw', help='Type of return data (json, pickle, raw)')
@click.option('-s', '--socket', required=False, help='Name of socket associated with the task to run')
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

        if not _task.code:
            print("Task must have code or specify socket.")
            return

        result = exec(_task.code, mymodule.__dict__)

        if result:
            print(result)
        return

    socket = Socket(name=socket)

    if data:
        result = socket(data)
    else:
        #
        # code = sys.stdin.read()
        # Determine mime type from code bytes
        # depickle or load json
        #
        lines = []
        for line in sys.stdin:
            stripped = line.strip()
            if not stripped:
                break
            lines.append(stripped)

        result = socket(''.join(lines))

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
        processor.branch = click.prompt('Branch',
                                        type=str, default=processor.branch)

    if not beat:
        processor.beat = click.prompt('Beat',
                                      type=bool, default=processor.beat)

    argspec = inspect.getargvalues(inspect.currentframe())
    _locals = argspec.locals
    processor = update_object(processor, _locals)
    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()


@add.command(name='log')
@click.option('-i', '--id', default=None, help="id of object")
@click.option('-s', '--source', default=None, required=False, help='Source name')
@click.option('-t', '--text', default=None, required=False, help='Text of log')
def add_log(context, id, source, text):

    pass


@add.command(name='task')
@click.option('-n', '--name', prompt=True, required=True, default=None, help="Name of this task")
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
    from sqlalchemy.orm import Session

    id = context.obj['id']
    user = context.obj['user']

    processor = ProcessorModel(
        id=id, status='ready', user_id=user.id, user=user, hostname=hostname, branch=branch, retries=retries, gitrepo=gitrepo, beat=beat, commit=commit, concurrency=workers, requested_status=requested_status, name=name, module=module)

    log1 = LogModel(oid=id, text='This is a log for '+name, user_id=user.id, public=True, user=user,
                    discriminator='ProcessorModel', source='pyfi')
    log2 = LogModel(oid=id, text='This is a log for '+name+' too', public=False, user_id=user.id, user=user,
                    discriminator='ProcessorModel', source='pyfi')

    context.obj['database'].session.add(log1)
    context.obj['database'].session.add(log2)

    processor.logs += [log1]
    processor.logs += [log2]
    processor.updated = datetime.now()

    context.obj['database'].session.add(processor)
    context.obj['database'].session.commit()

    print(processor)


@add.command(name='privilege')
@click.option('-u', '--user', default=None, required=True)
@click.option('-n', '--name', default=None, required=True)
@click.option('-r', '--role', default=None, required=False)
@click.pass_context
def add_privilege(context, user, name, role):
    """
    Add privilege to the database
    """
    from sqlalchemy.exc import IntegrityError

    if user is None and role is None:
        print("User and Role cannot both be None.")
        return

    id = context.obj['id']

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        try:
            user = context.obj['database'].session.query(
                UserModel).filter_by(name=user).first()
            user.lastupdated = datetime.now()
            privilege = PrivilegeModel(id=id, name=name, right=name)
            user.privileges += [privilege]
            context.obj['database'].session.add(privilege)
            context.obj['database'].session.add(user)
            context.obj['database'].session.commit()
            print("Privilege added")
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
    import hashlib

    id = context.obj['id']

    if name is None or email is None:
        raise click.UsageError("Name and Email are required")

    try:
        _password = hashlib.md5(password.encode()).hexdigest()
        # This user will be used in OSO authorizations
        user = UserModel(name=name, owner=name,
                         password=_password, clear=password, email=email)
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

    processor = context.obj['database'].session.query(
        ProcessorModel).filter_by(id=socket.processor_id).first()
    if not interval and interval > 0:
        socket.interval = click.prompt('Interval',
                                       type=int, default=socket.interval)
        processor.requested_status = 'update'

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
@click.option('-s', '--source', default=None, required=True, help="Source socket name")
@click.option('-t', '--target', default=None, required=True, help="Target socket name")
@click.option('-pi', '--procid', default=None, required=False, help="Processor id")
@click.option('-pn', '--procname', default=None, required=False, help="Processor name")
@click.pass_context
def add_plug(context, name, queue, source, target, procid, procname):
    """
    Add plug to a processor
    """
    id = context.obj['id']

    source_socket = context.obj['database'].session.query(
        SocketModel).filter_by(name=source).first()

    target_socket = context.obj['database'].session.query(
        SocketModel).filter_by(name=target).first()

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

    plug.source = source_socket
    plug.target = target_socket
    plug.queue = queue
    plug.updated = datetime.now()
    processor.plugs += [plug]

    context.obj['database'].session.add(source_socket)
    context.obj['database'].session.add(target_socket)
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
def add_socket(context, name, queue, interval, procname, task):
    """
    Add socket to a processor
    """
    id = context.obj['id']

    processor = context.obj['database'].session.query(
        ProcessorModel).filter_by(name=procname).first()

    queue = context.obj['database'].session.query(
        QueueModel).filter_by(name=queue).first()

    user = context.obj['user']

    socket = SocketModel(name=name, id=id, user=user, user_id=user.id, requested_status='create', interval=interval,
                         status='ready', processor_id=processor.id)

    if task is not None:
        _task = context.obj['database'].session.query(
            TaskModel).filter_by(name=task).first()
        if _task is None:
            _task = TaskModel(name=task, module=processor.module,
                              gitrepo=processor.gitrepo)
        socket.task = _task
        context.obj['database'].session.add(_task)

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
    Commands for remote agent management
    """
    pass


@agent.command(name='stop')
@click.pass_context
def stop_agent(context):
    """ Stop an agent """
    pass



@worker.command(name='start', help='Start a pyfi worker')
@click.option('-n', '--name', required=True, help="Name of worker")
@click.option('-p', '--pool', default=1, required=False, help="Size of worker pool")
@click.option('-s', '--skip-venv', is_flag=True, default=False, required=False, help="Skip building the virtual environment")
@click.option('-q', '--queue', default=1, help='Maximum number of messages on worker internal queue')
@click.pass_context
def start_worker(context, name, pool, skip_venv, queue):
    from pyfi.worker import Worker

    workerModel = context.obj['database'].session.query(
        WorkerModel).filter_by(name=name).first()

    worker = {}
    processor = context.obj['database'].session.query(
        ProcessorModel).filter_by(id=workerModel.processor_id).first()

    dir = 'work/'+processor.id
    os.makedirs(dir, exist_ok=True)

    workerproc = Worker(
        processor, workdir=dir, pool=pool, size=queue, database=context.obj['dburi'], skipvenv=skip_venv, celeryconfig=None, backend=CONFIG.get('backend', 'uri'), broker=CONFIG.get('broker', 'uri'))

    wprocess = workerproc.start()

    processor.worker.requested_status = 'ready'
    processor.worker.status = 'running'
    context.obj['database'].session.add(
        processor.worker)

    context.obj['database'].session.commit()
    wprocess.join()


@ls.command(name='queue')
@click.option('--id', default=None, help="ID of call")
@click.option('-n', '--name', default=None, required=False, help='Name of queue')
@click.option('-t', '--task', default=None, required=False, help='Name of task')
@click.pass_context
def ls_queue(context, id, name, task):
    """
    List a queue
    """
    from urllib.parse import urlparse

    # Combine info from database and rabbitmq about this queue
    import requests

    if id is not None:
        queue = context.obj['database'].session.query(
            QueueModel).filter_by(id=id).first()
    elif name is not None:
        queue = context.obj['database'].session.query(
            QueueModel).filter_by(name=name).first()

    if task:
        # Query for task, get task name, processor name and queue name
        # to combine into queuname.procname.taskname
        # Then return info about queuename and queuname.procname.taskname from broker
        pass
    if queue is None:
        queuename = name
    else:
        queuename = queue.name

    user = CONFIG.get('broker', 'user')
    password = CONFIG.get('broker', 'password')
    api = CONFIG.get('broker', 'api')

    session = requests.Session()
    session.auth = (user, password)

    apiurl = urlparse(api)

    auth = session.post(apiurl.scheme+"://"+apiurl.netloc)
    response = session.get(
        api+"/queues/#/"+queuename)
    print(response.content)


@ls.command(name='call')
@click.option('--id', default=None, help="ID of call")
@click.option('-n', '--name', default=None, required=False, help='Name of call')
@click.option('-r', '--result', default=False, is_flag=True, help="Show result of call")
@click.option('-t', '--tree', default=False, is_flag=True, help="Show forward call tree")
@click.option('-g', '--graph', default=False, is_flag=True, help="Show complete call graph")
@click.option('-f', '--flow', default=False, is_flag=True, help="Show all calls in a workflow")
@click.pass_context
def ls_call(context, id, name, result, tree, graph, flow):
    """
    List a call
    """
    import redis
    import json

    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated",
             "Socket", "Started", "Finished", "State"]
    x.field_names = names

    calls = None
    call = None

    if name is None and id is None:
        print("Must provide name or id. See $ pyfi ls call --help")
        return

    if name is not None:
        calls = context.obj['database'].session.query(
            CallModel).filter_by(name=name).all()
    elif id is not None:
        call = context.obj['database'].session.query(
            CallModel).filter_by(id=id).first()
        if call is None:
            print("No call with that id.")
            return
        if flow:  # task_id is NOT unique to each workflow invocation
            # Should use tracking
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
                        _child_node = get_call_graph(
                            _child_node, _child, _calls)

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
    print()

    print("Provenance")
    names = ["Task", "Task Parent", "Flow Parent"]
    x.field_names = names
    x.add_row([node.celeryid, node.taskparent, node.parent])
    print(x)
    x = PrettyTable()

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        print()
        print('Events')
        names = ["Name", "ID", "Owner", "Last Updated", "Note"]
        x.field_names = names
        if call:
            for event in call.events:
                x.add_row([event.name, event.id, event.owner,
                           event.lastupdated, event.note])
    print(x)


@ls.command(name="roles")
@click.option('-p', '--page', default=1, required=False)
@click.option('-r', '--rows', default=10, required=False)
@click.option('-a', '--ascend', default=False, is_flag=True, required=False)
@click.pass_context
def ls_roles(context, page, rows, ascend):
    """
    List roles
    """
    x = PrettyTable()

    names = ["Page", "Row", "Name", "ID", "Owner",
             "Last Updated", "Created"]
    x.field_names = names

    total = context.obj['database'].session.query(RoleModel).count()

    if total == 0:
        print("No data yet.")
        return

    if total > rows and page > round(total/rows):
        print("Only {} pages exist.".format(round(total/rows)))
        return

    if not ascend:
        if total < rows:
            nodes = context.obj['database'].session.query(
                RoleModel).all()
        else:
            nodes = context.obj['database'].session.query(
                RoleModel).order_by(RoleModel.lastupdated.desc()).offset((page-1)*rows).limit(rows)
    else:
        if total < rows:
            nodes = context.obj['database'].session.query(
                RoleModel).all()
        else:
            nodes = context.obj['database'].session.query(
                RoleModel).order_by(RoleModel.lastupdated.asc()).offset((page-1)*rows).limit(rows)

    row = 0
    for node in nodes:
        row += 1
        x.add_row([page, row, node.name, node.id, node.owner,
                  node.lastupdated, node.created])

    print(x)

    if total > 0:
        print("Page {} of {} of {} total records".format(
            page, round(total/rows), total))
    else:
        print("No rows")


@ls.command(name='jobs')
@click.option('-n', '--name', default=None, required=False, help='Name of processor')
@click.pass_context
def ls_jobs(context, name, page, rows, ascend):
    """ List scheduled jobs """
    pass


@ls.command(name='job')
@click.pass_context
def ls_job(context, name, id):
    """ List a job """
    pass


@ls.command(name='calls')
@click.option('-p', '--page', default=1, required=False)
@click.option('-r', '--rows', default=10, required=False)
@click.option('-u', '--unfinished', is_flag=True, default=False, required=False)
@click.option('-a', '--ascend', default=False, is_flag=True, required=False)
@click.pass_context
def ls_calls(context, page, rows, unfinished, ascend):
    """
    List queues
    """
    x = PrettyTable()

    names = ["Page", "Row", "Name", "ID", "Owner",
             "Last Updated", "Socket", "Started", "Finished", "State"]
    x.field_names = names

    if unfinished:
        total = context.obj['database'].session.query(
            CallModel).filter_by(finished=None).count()
    else:
        total = context.obj['database'].session.query(CallModel).count()

    if total == 0:
        print("No data yet.")
        return

    if total > rows and page > round(total/rows):
        print("Only {} pages exist.".format(round(total/rows)))
        return

    if not ascend:
        if total < rows:
            if unfinished:
                nodes = context.obj['database'].session.query(
                    CallModel).filter_by(finished=None).all()
            else:
                nodes = context.obj['database'].session.query(
                    CallModel).all()
        else:
            if unfinished:
                nodes = context.obj['database'].session.query(
                    CallModel).order_by(CallModel.lastupdated.desc()).filter_by(finished=None).offset((page-1)*rows).limit(rows)
            else:
                nodes = context.obj['database'].session.query(
                    CallModel).order_by(CallModel.lastupdated.desc()).offset((page-1)*rows).limit(rows)
    else:
        if total < rows:
            if unfinished:
                nodes = context.obj['database'].session.query(
                    CallModel).filter_by(finished=None).all()
            else:
                nodes = context.obj['database'].session.query(
                    CallModel).all()
        else:
            if unfinished:
                nodes = context.obj['database'].session.query(
                    CallModel).order_by(CallModel.lastupdated.asc()).filter_by(finished=None).offset((page-1)*rows).limit(rows)
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


@ls.command(name='network')
@click.option('-h', '--horizontal', default=False, is_flag=True, required=False, help="Horizontal tree mode")
@click.option('-v', '--vertical', default=False, is_flag=True, required=False, help="Vertical tree mode")
@click.option('-n', '--node', required=False, help="List network for node")
@click.pass_context
def ls_network(context, horizontal, vertical, node, condensed=True):
    """ List the PYFI network """

    from pptree import print_tree, Node
    
    if horizontal or vertical:
        condensed = False

    if node is not None:
        node = context.obj['database'].session.query(
            NodeModel).filter_by(name=node).first()
        nodes = [node]
    else:
        nodes = context.obj['database'].session.query(NodeModel).all()

    root = Node("PYFI")

    for node in nodes:
        node_node = Node("node::"+node.name, root)
        if condensed:
            print("node::"+node.name)
        agent = node.agent
        agent_node = Node("agent::"+agent.name, node_node)
        if condensed:
            print("  agent::"+agent.name)
        worker_node = Node("worker::"+agent.worker.name, agent_node)
        if condensed:
            print("    worker::"+agent.worker.name)
        processor_node = Node(
            "processor::"+agent.worker.processor.name, worker_node)
        if condensed:
            print("      processor::"+agent.worker.processor.name)

        for socket in agent.worker.processor.sockets:
            socket_node = Node("socket::"+socket.name, processor_node)
            if condensed:
                print("        socket::"+socket.name)
            task_node = Node("task::"+socket.task.name, socket_node)
            if condensed:
                print("          task::"+socket.task.name)
            module_node = Node("module::"+socket.task.module, task_node)
            if condensed:
                print("            module::"+socket.task.module)
            function_node = Node("function::"+socket.task.name, task_node)
            if condensed:
                print("            function::"+socket.task.name)

    if not condensed:
        print_tree(root, horizontal=horizontal)


@ls.command(name='work')
@click.pass_context
def ls_work(context):
    """
    List work submissions
    """

    # Work is defined as the submission of a task along with scheduling requirements for a
    # scheduler to place into the network for processing.
    # Work can also define a "job schedule" which means specific times or intervals a task is to be
    # executed.
    # A work object refers to things by name. e.g. I want to run "task A" or invoke "Socket B->Plug B"
    # It's the schedulers job to convert the names to objects and assign the work to a processor
    # A work object can refer to a task with code - or, a task that is not linked to by a plug and socket (i.e. part of a flow)

    # Worker objects will pull from the work table when their own queues are empty.

    # Work objects should not be confused with Job objects. Job objects are specific to APScheduler
    # and represent scheduled jobs that invoke specific tasks.
    # However, a work object can result in a scheduled job being created.
    pass


@ls.command(name='worker')
@click.pass_context
def ls_worker(context):
    """
    List a worker
    """
    pass


@ls.command(name='socket')
@click.option('--id', default=None, help="ID of call")
@click.option('-n', '--name', default=None, required=False, help='Name of call')
@click.option('-g', '--graph', default=False, is_flag=True, help="Show complete call graph")
@click.pass_context
def ls_socket(context, id, name, graph):
    """
    List a socket
    """
    if name is not None:
        socket = context.obj['database'].session.query(
            SocketModel).filter_by(name=name).first()
    elif id is not None:
        socket = context.obj['database'].session.query(
            SocketModel).filter_by(id=id).first()

    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Module", "Task", "Last Updated",
             "Status", "Processor", "Queue", "Interval"]

    x.field_names = names

    sockets = [socket]

    for node in sockets:
        x.add_row([node.name, node.id, node.owner, node.task.module, node.task.name, node.lastupdated,
                  node.status, node.processor.name, node.queue.name, node.interval])

    from pptree import print_tree, Node

    root = Node(socket.name)
    module = Node(socket.task.module, root)
    task = Node(socket.task.name, module)

    if graph:
        print_tree(root, horizontal=False)
    else:
        print(x)


@ls.command(name='scheduler')
@click.pass_context
def ls_scheduler(context):
    """
    List a scheduler
    """
    pass


@ls.command(name='processor')
@click.option('--id', default=None, help="ID of call")
@click.option('-n', '--name', default=None, required=False, help='Name of call')
@click.option('-g', '--graph', default=False, is_flag=True, help="Show complete call graph")
@click.pass_context
def ls_processor(context, id, name, graph):
    """
    List a processor
    """
    from pptree import print_tree, Node

    if name is not None:
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(name=name).first()
    elif id is not None:
        processor = context.obj['database'].session.query(
            ProcessorModel).filter_by(id=id).first()

    if processor is None:
        print("No processor found.")
        return

    workername = processor.worker.name if processor.worker else "None"

    sockets = processor.sockets
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Module", "Task", "Last Updated",
             "Status", "Processor", "Queue", "Interval"]

    x.field_names = names

    root = Node(processor.name)
    for node in sockets:
        x.add_row([node.name, node.id, node.owner, node.task.module, node.task.name, node.lastupdated,
                  node.status, node.processor.name, node.queue.name, node.interval])

        sock = Node(node.name, root)
        module = Node(node.task.module, sock)
        task = Node(node.task.name, module)

    if graph:
        print_tree(root, horizontal=False)
    else:
        print("Name:", processor.name)
        print("ID:", processor.id)
        print("Module:", processor.module)
        print("Workername:", workername)
        print("Hostname:", processor.hostname)
        print("Owner:", processor.owner)
        print("Last Updated:", processor.lastupdated)
        print("Requested Status:", processor.requested_status)
        print("Status:", processor.name)
        print("Concurrency:", processor.concurrency)
        print("Beat:", processor.beat)
        print("Git Repo:", processor.gitrepo)
        print("Name:", processor.name)

    print()
    print("Sockets")
    print(x)

    x = PrettyTable()

    names = ["Created", "Text", "Source"]

    x.field_names = names

    for log in processor.logs:
        x.add_row([log.created, log.text, log.source])

    print()
    print("Logs")
    print(x)


@ls.command(name='task')
@click.pass_context
def ls_task(context):
    """
    List a task
    """
    pass


@ls.command(name='stats')
@click.pass_context
def ls_stats(context):
    """
    List object stats
    """
    pass


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

    names = ["Name", "ID", "Host", "Owner", "Last Updated",
             "CPUs", "Mem Size", "Free Mem", "Used Mem", "Agent"]
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
             "Requested Status", "Broadcast Queue", "Status", "Type"]
    x.field_names = names
    queues = context.obj['database'].session.query(QueueModel).all()
    for node in queues:
        x.add_row([node.name, node.id, node.owner, node.lastupdated, node.message_ttl, node.expires,
                  node.requested_status, node.name+".topic", node.status, node.qtype])

    print(x)


@ls.command(name='users')
@click.pass_context
def ls_users(context):
    """
    List users
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Email", "Password"]
    x.field_names = names

    w = context.obj['database'].session.execute("select current_user").first()
    users = context.obj['database'].session.query(UserModel).all()
    for user in users:
        x.add_row([user.name, user.id, user.owner, user.email, user.password])

    print(x)


@ls.command(name='role')
@click.option('-n', '--name', default=None, required=True)
@click.pass_context
def ls_role(context, name):
    """ List a role"""
    import warnings

    x = PrettyTable()
    names = ["Name", "Last Updated", "By"]
    x.field_names = names

    roles = []

    role = context.obj['database'].session.query(
        RoleModel).filter_by(name=name).first()

    if role is None:
        print("No role found.")
        return
    else:
        roles = [role]

    for role in roles:
        x.add_row([role.name, role.lastupdated, role.owner])

        print(x)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)

        x = PrettyTable()
        print()
        print("Privileges")
        names = ["Name", "Permission", "Last Updated", "By"]
        x.field_names = names

        for priv in role.privileges:
            x.add_row([priv.name, priv.right, priv.lastupdated, priv.owner])

        print(x)


@ls.command(name='user')
@click.option('-n', '--name', default=None, required=True)
@click.pass_context
def ls_user(context, name):
    """
    List a user
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Email"]
    x.field_names = names
    user = context.obj['database'].session.query(
        UserModel).filter_by(name=name).first()
    x.add_row([user.name, user.id, user.owner, user.email])

    print(x)

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)

        x = PrettyTable()
        print()
        print("Roles")
        names = ["Name", "Role", "Last Updated", "By"]
        x.field_names = names

        for role in user.roles:
            x.add_row([user.name, role.name, role.lastupdated, role.owner])

        print(x)

        x = PrettyTable()
        print()
        print("Privileges")
        names = ["Name", "Permission", "Last Updated", "By"]
        x.field_names = names

        for priv in user.privileges:
            x.add_row([user.name, priv.right, priv.lastupdated, priv.owner])

        print(x)

        x = PrettyTable()
        print()
        print("Revoked Privileges")
        names = ["Name", "Permission", "Last Updated", "By"]
        x.field_names = names

        for priv in user.revoked:
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
             "Requested Status", "Status", "Agent", "Backend", "Broker", "Hostname", "Processor"]
    x.field_names = names
    workers = context.obj['database'].session.query(WorkerModel).all()

    for node in workers:
        x.add_row([node.name, node.id, node.owner, node.lastupdated,
                  node.requested_status, node.status, node.agent.name, node.backend, node. broker, node.hostname, node.processor.name])

    print(x)


@ls.command(name='processors')
@click.option('-g', '--gitrepo', is_flag=True, default=False)
@click.option('-c', '--commit', is_flag=True, default=False)
@click.option('-m', '--module', is_flag=True, default=False)
@click.option('-o', '--owner', is_flag=True, default=False)
@click.pass_context
def ls_processors(context, gitrepo, commit, module, owner):
    """
    List processors
    """
    processors = context.obj['database'].session.query(ProcessorModel).all()
    x = PrettyTable()

    names = ["Name", "ID", "Module", "Worker", "Host", "Owner", "Last Updated",
             "Requested Status", "Status", "Concurrency", "Beat"]

    if gitrepo:
        names += ["Git"]
    if module:
        names += ["Module"]
    if owner:
        names += ["Owner"]
    if commit:
        names += ["Commit"]

    x.field_names = names

    for processor in processors:
        workername = processor.worker.name if processor.worker else "None"
        row = [processor.name, processor.id, processor.module, workername, processor.hostname, processor.owner, processor.lastupdated,
               processor.requested_status, processor.status, processor.concurrency, processor.beat]

        if gitrepo:
            row += [processor.gitrepo]
        if module:
            row += [processor.module]
        if owner:
            row += [processor.owner]
        if commit:
            row += [processor.commit]

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
        values = [node.name, node.id, node.owner,
                  node.lastupdated, node.module]

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
             "Status", "Processor", "Queue", "Type", "Interval"]
    x.field_names = names
    sockets = context.obj['database'].session.query(SocketModel).all()

    for node in sockets:
        x.add_row([node.name, node.id, node.owner, node.task.module, node.task.name, node.lastupdated,
                  node.status, node.processor.name, node.queue.name, node.schedule_type, node.interval])

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
             "Status", "Queue", "Source Task", "Target Task", "Source Socket", "Target Socket"]
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
    print("Listening to", name)
    func = None
    if adaptor:
        module = importlib.import_module('.'.join(adaptor.rsplit('.')[:-1]))
        _class = getattr(module, adaptor.rsplit('.')[-1:][0])
        print("Loaded adaptor function", adaptor)
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
    name = context.obj['user'].name if context.obj['user'] is not None else None

    loginstr = "Not logged in"
    if name is not None:
        loginstr = "Logged into PYFI as "+name
    print("Database user {}.\n{}.".format(context.obj['owner'], loginstr))


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
@click.option('-p', '--pool', default=1, help='Process pool for message dispatches')
@click.option('-s', '--size', default=10, help='Maximum number of messages on worker internal queue')
@click.option('-h', '--host', help='Remote hostname to start the agent via ssh')
@click.option('-p', '--path', help='Remote PATH to use')
@click.pass_context
def start_agent(context, port, clean, backend, broker, config, queues, user, pool, size, host, path):
    """
    Run pyfi agent server
    """
    from pyfi.agent import Agent

    if host is not None:
        """
        _ssh = paramiko.SSHClient()
        _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh.connect(hostname=hostname, username=username,
                        key_filename=sshkey)
        command = "python3.8 -m venv {}; export LLVM_CONFIG=/usr/bin/llvm-config-10; {}/bin/pip install --upgrade py-entangle".format(
            env, env)
        _, stdout, _ = _ssh.exec_command(command)
        """
    else:
        agent = Agent(context.obj['database'], context.obj['dburi'], port, pool=pool,
                    config=config, backend=backend, user=user, clean=clean, size=size, broker=broker)
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
