"""
cli.py - pyfi CLI command tool for managing database
"""
import configparser
import getpass
import hashlib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s: "
    "%(levelname)s: "
    "%(funcName)s(): "
    "%(lineno)d:\t"
    "%(message)s",
)


logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy_oso.session").setLevel(logging.CRITICAL)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
import os
import platform
import sys
from datetime import datetime
from pathlib import Path

import click
from prettytable import PrettyTable
from sqlalchemy import MetaData, create_engine, event
from sqlalchemy import exc as sa_exc
from sqlalchemy import literal_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy_oso import authorized_sessionmaker

from pyfi.db.model import (
    AgentModel,
    ArgumentModel,
    CallModel,
    DeploymentModel,
    EventModel,
    LoginModel,
    LogModel,
    NetworkModel,
    NodeModel,
    PasswordModel,
    PlugModel,
    ProcessorModel,
    QueueModel,
    RoleModel,
    SchedulerModel,
    SocketModel,
    TaskModel,
    UserModel,
    WorkerModel,
    oso,
)
from pyfi.db.model.models import PrivilegeModel
from pyfi.web import run_http

HOSTNAME = platform.node()

current_user = getpass.getuser()

home = str(Path.home())

CONFIG = configparser.ConfigParser()

HOME = str(Path.home())
ini = HOME + "/pyfi.ini"
CONFIG.read(ini)

dburi = CONFIG.get("database", "uri")

POSTGRES_ROOT = (
    "/".join(dburi.rsplit("/")[:-1]) + "/"
)  # "postgresql://postgres:pyfi101@" + HOSTNAME + ":5432/"
POSTGRES = dburi  # "postgresql://postgres:pyfi101@" + HOSTNAME + ":5432/pyfi"


def handle_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception %s", exc_value)


def import_class(name):
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


@click.group(invoke_without_command=True)
@click.option("--debug", is_flag=True, default=False, help="Debug switch")
@click.option("-d", "--db", help="Database URI")
@click.option("--backend", help="Task queue backend")
@click.option("--broker", help="Message broker URI")
@click.option("-a", "--api", help="Message broker API URI")
@click.option("-u", "--user", help="Message broker API user")
@click.option("-p", "--password", help="Message broker API password")
@click.option(
    "-i", "--ini", default=home + "/pyfi.ini", help="flow .ini configuration file"
)
@click.option("-c", "--config", default=False, is_flag=True, help="Configure pyfi")
@click.pass_context
def cli(context, debug, db, backend, broker, api, user, password, ini, config):
    """
    CLI for creating & managing flow networks
    """

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if debug:
        logging.basicConfig(
            format="%(asctime)s : %(name)s %(levelname)s : %(message)s",
            level=logging.DEBUG,
        )
    else:
        logging.basicConfig(
            format="%(asctime)s : %(name)s %(levelname)s : %(message)s",
            level=logging.INFO,
        )

    context.obj = {}
    # If login section, then query for User and see if token matches and still valid
    if config:
        if not db:
            db = click.prompt("Database connection URI", type=str, default=POSTGRES)
        if not backend:
            backend = click.prompt(
                "Result backend URI", type=str, default="redis://localhost"
            )
        if not broker:
            broker = click.prompt(
                "Message broker URI", type=str, default="pyamqp://localhost"
            )
        if not api:
            api = click.prompt(
                "Message broker API", type=str, default="http://localhost:15672/api"
            )
        if not user:
            user = click.prompt(
                "Message broker API username", type=str, default="guest"
            )
        if not password:
            password = click.prompt(
                "Message broker API password", type=str, default="guest"
            )

        email = click.prompt("Postgres user email", type=str, default="p@e")
        password = click.prompt("Postgres user password", type=str, default="pyfi101")

        _password = hashlib.md5(password.encode()).hexdigest()

        _config = configparser.ConfigParser()

        _config.add_section("login")

        _config.set("login", "password", _password)
        _config.set("login", "user", "postgres")

        _config.add_section("database")
        _config.set("database", "uri", db)

        _config.add_section("backend")
        _config.set("backend", "uri", backend)

        _config.add_section("broker")
        _config.set("broker", "uri", broker)
        _config.set("broker", "api", api)
        _config.set("broker", "user", user)
        _config.set("broker", "password", password)

        with open(home + "/pyfi.ini", "w") as configfile:
            _config.write(configfile)

        print("Configuration file created at {}".format(home + "/pyfi.ini"))

    if not os.path.exists(ini) and db is None:
        print("No database uri configured. Please run \033[1m $ pyfi --config")
        exit(1)

    # If there is a user login in pyfi.ini then construct the DB URI
    # using their login info

    if os.path.exists(ini) and db is None:
        CONFIG.read(ini)
        db = CONFIG.get("database", "uri")

    # If there is a pyfi.ini file in users home directory
    # if db is None then check the .pyfi property file
    context.obj["dburi"] = db

    try:
        engine = create_engine(db, isolation_level="READ UNCOMMITTED")
        engine.uri = db
        session = sessionmaker(bind=engine)()

        context.obj["database"] = engine
        context.obj["session"] = session
        engine.session = session

        context.obj["owner"] = session.query(literal_column("current_user")).first()[0]

    except:
        import traceback

        print(traceback.format_exc())
        print(
            "Database unavailable. Please check your configuration or ensure database server is running."
        )
        return

    if CONFIG.has_section("login"):
        username = CONFIG.get("login", "user")
        password = CONFIG.get("login", "password")

        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=sa_exc.SAWarning)
            try:
                # engine = create_engine(db)
                # engine.uri = db
                session = sessionmaker(bind=engine)()

                user_m = (
                    session.query(UserModel)
                    .filter_by(name=username, password=password)
                    .first()
                )
                # context.obj['user'] = user_m
                # context.obj['database'].session.add(user_m)
                if username is None:
                    return

                if user_m is None:
                    print(f"Unable to log in {username}.")
                    return

                logger.debug(f"{user_m.name} logged in.")

                session.expunge(user_m)
            except:
                context.obj["user"] = None
                print(f"Unable to log in {username}..")
                return

            finally:
                session.close()

        context.obj["database"].session.close()

        """ RBAC """
        oso.load_files([home + "/pyfi.polar"])

        def get_checked_permissions(*args, **kwargs):
            logger.debug("cli: get_checked_permissions")

            session = sessionmaker(bind=engine)()
            _user = (
                session.query(UserModel)
                .filter_by(name=username, password=password)
                .first()
            )
            permissions = {
                SchedulerModel: "read",
                PrivilegeModel: "read",
                AgentModel: "read",
                NodeModel: "read",
                EventModel: "read",
                CallModel: "read",
                TaskModel: "read",
                QueueModel: "read",
                SocketModel: "read",
                PasswordModel: "read",
                PlugModel: "read",
                WorkerModel: "read",
                LogModel: "read",
                UserModel: "read",
                ArgumentModel: "read",
                DeploymentModel: "read",
                ProcessorModel: "read",
                RoleModel: "read",
                NetworkModel: "read",
            }

            for privilege in _user.privileges:
                if privilege.right == "READ_LOG":
                    permissions[LogModel] = "read"

            session.close()

            return permissions

        user_object = None

        context.obj["session"] = session = authorized_sessionmaker(
            get_oso=lambda: oso,
            get_user=lambda: user_m,
            get_checked_permissions=get_checked_permissions,
            bind=engine,
        )()

        """ RBAC """

        user_m2 = user_object = (
            session.query(UserModel).filter_by(name=username, password=password).first()
        )
        # Add the logged in user to the authorized_session
        # context.obj['database'].session.merge(user_m)
        session.add(user_m2)
        context.obj["user"] = user_m2
        context.obj["database"].session = session  # context.obj['session']

        @event.listens_for(session, "after_commit")
        def receive_after_commit(session):
            """Invoked after every transaction commit"""
            import json

            import redis

            logging.debug("commit UPDATED", session)
            redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

            for obj in session:
                logging.debug("OBJ IN SESSION", type(obj), obj)

                if isinstance(obj, ProcessorModel):
                    # Publish to redis, pubsub, which gets sent to browser
                    redisclient.publish(
                        "global",
                        json.dumps({"type": "processor", "processor": str(obj)}),
                    )

        # Generate OSO user policy file based on roles and privileges in the database
        # Then load the policy file into oso

        # Update database URI based on logged in user
    else:
        context.obj["user"] = None

    if len(sys.argv) == 1:
        click.echo(context.get_help())


@cli.group()
def user():
    """
    User commands
    """
    pass


@user.command(name="remove")
@click.option("-u", "--user", default=None, required=True)
@click.option("-r", "--role", default=None, required=False)
@click.option("-p", "--privilege", default=None, required=False)
@click.pass_context
def user_remove(context, user, role, privilege):
    """
    Remove roles and privileges from a user
    """
    return


@user.command(name="add")
@click.option("-u", "--user", default=None, required=True)
@click.option("-r", "--role", default=None, required=False)
@click.option("-p", "--privilege", default=None, required=False)
@click.pass_context
def user_add(context, user, role, privilege):
    """
    Add roles and privileges to a user
    """
    user_m = (
        context.obj["database"].session.query(UserModel).filter_by(name=user).first()
    )
    if role:
        role_m = (
            context.obj["database"]
            .session.query(RoleModel)
            .filter_by(name=role)
            .first()
        )
        print("ROLE:", role_m)
        user_m.roles += [role_m]
        database = context.obj["database"]
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
    """Manage declarative infrastructure files"""


@compose.command(name="kill")
@click.argument("filename")
@click.pass_context
def compose_kill(context, filename):
    """Kill a running infrastructure"""
    import yaml
    from pyfi.yaml.builder import stop_network

    with open(filename, "r") as stream:
        try:
            detail = yaml.safe_load(stream)
            stop_network(detail)
        except yaml.YAMLError as exc:
            print(exc)


@compose.command(name="build")
@click.option("-f", "--file", default="pyfi.yaml", required=False)
@click.option("-d", "--deploy", is_flag=True, default=False, help="Deploy the network")
@click.argument("nodes", nargs=-1)
@click.pass_context
def compose_build(context, file, deploy, nodes):
    """Build infrastructure from a yaml file"""
    import yaml
    from pyfi.yaml.builder import compose_network

    with open(file, "r") as stream:
        try:
            detail = yaml.safe_load(stream)
            compose_network(detail, command="build", deploy=deploy, nodes=list(nodes))
        except yaml.YAMLError as exc:
            print(exc)


@cli.command()
def logout():
    """Logout current user"""
    ini = home + "/pyfi.ini"

    if CONFIG.has_option("login", "user"):
        CONFIG.remove_section("login")
        print("Logged out.")

    with open(ini, "w") as inifile:
        CONFIG.write(inifile)


@cli.command()
@click.pass_context
@click.option(
    "-d", "--database", is_flag=True, default=False, help="Database login only"
)
def login(context, database):
    """
    Log into flow CLI
    """
    import hashlib
    from urllib.parse import urlparse

    ini = home + "/pyfi.ini"

    user = None

    if context.obj["user"] is not None:
        print("Please logout first.")
        return

    if CONFIG.has_option("login", "user"):
        _user = CONFIG.get("login", "user")
    else:
        CONFIG.add_section("login")

    password = None
    if CONFIG.has_option("login", "password"):
        _password = CONFIG.get("login", "password")

    user = click.prompt("User", type=str)
    __password = click.prompt("Password", type=str)
    password = hashlib.md5(__password.encode()).hexdigest()

    CONFIG.set("login", "user", user)

    if not database:
        user_m = (
            context.obj["database"]
            .session.query(UserModel)
            .filter_by(name=user, password=password)
            .first()
        )

        if user_m is not None:
            _login = LoginModel(user=user_m)
            context.obj["database"].session.add(_login)
            context.obj["database"].session.commit()
            print("Logged in.")
        else:
            print("Invalid login.")

    dburi = CONFIG.get("database", "uri")
    uri = urlparse(dburi)
    newuri = (
        uri.scheme
        + "://"
        + user
        + ":"
        + __password
        + "@"
        + uri.hostname
        + ":"
        + str(uri.port)
        + uri.path
    )
    CONFIG.set("database", "uri", newuri)
    CONFIG.set("login", "password", password)

    with open(ini, "w") as inifile:
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
@click.option("-t", "--to", required=True)
@click.pass_context
def clone(context, to):
    """
    Clone the current virtual environment to the node host --to
    """
    pass


@cli.group()
@click.option("--id", default=None, help="ID of processor")
@click.pass_context
def proc(context, id):
    """
    Run or manage processors
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj["id"] = str(id)


@cli.group()
@click.pass_context
def db(context):
    """
    Database operations
    """
    pass


@cli.group()
@click.pass_context
def network(context):
    """
    Network operations
    """
    pass


@network.command(name="add")
@click.option("-n", "--name", help="Name of network")
@click.option("-nd", "--node", help="Name of node to add")
@click.pass_context
def add_node_to_network(context, name, node):
    """Add node to a network"""
    network = (
        context.obj["database"].session.query(NetworkModel).filter_by(name=name).first()
    )
    logging.debug("network is %s", network)
    node = context.obj["database"].session.query(NodeModel).filter_by(name=node).first()
    logging.debug("node is %s", node)
    if node is None:
        print(f"Node {node} not found.")
        return

    network.nodes += [node]

    logging.debug("committing")
    context.obj["database"].session.commit()
    logging.debug("committed")
    print(f"Node {node.name} added to network {network.name}")


@db.command()
@click.option(
    "-d", "--directory", default="migrations", help="Directory of migration pyfi agent"
)
@click.pass_context
def migrate(context, directory):
    """
    Perform database migration/upgrade
    """
    from alembic.autogenerate import compare_metadata, produce_migrations
    from alembic.migration import MigrationContext

    from pyfi.db.model import Base

    target_metadata = Base.metadata

    engine = context.obj["database"]

    mc = MigrationContext.configure(engine.connect())
    diff = compare_metadata(mc, target_metadata)
    script = produce_migrations(mc, target_metadata)

    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", directory)
    alembic_cfg.set_main_option("sqlalchemy.url", context.obj["dburi"])
    command.upgrade(alembic_cfg, "head")


@db.command(help="Drop and rebuild database tables")
@click.option("-y", "--yes", is_flag=True, prompt=True, help="Yes to rebuild now")
@click.pass_context
def rebuild(context, yes):
    if yes:

        if CONFIG.has_section("login"):
            CONFIG.remove_section("login")

        dropdb(context)
        context.invoke(db_init)


def dropdb(context):
    from pyfi.db.model import Base

    # For every user in "user" table, DROP USER name

    _users = [u.name for u in context.obj["database"].session.query(UserModel).all()]

    for user in _users:
        if user != "postgres":
            context.obj["database"].session.execute(f"DROP OWNED BY {user}")
            context.obj["database"].session.execute(f"DROP USER {user}")
            print("Dropped user {}".format(user))

    context.obj["database"].session.commit()

    for t in Base.metadata.sorted_tables:
        try:
            print("Dropping {}".format(t.name))
            t.drop(context.obj["database"])
            print("Dropped {}".format(t.name))
        except:
            import traceback

            print(traceback.format_exc())

    print("Database dropped.")


@db.command(name="drop")
@click.option(
    "-y", "--yes", is_flag=True, default=False, help="Yes to rebuild without prompting"
)
@click.pass_context
def db_drop(context, yes):
    """
    Drop all database tables
    """
    try:
        if not yes:
            if click.confirm(
                "Are you sure you want to drop the database?", default=False
            ):
                if click.confirm(
                    "Are you REALLY sure you want to drop the database?", default=False
                ):
                    dropdb(context)
                else:
                    print("Operation aborted.")
            else:
                print("Operation aborted.")

        # Drop roles
    except Exception as ex:
        logging.error(ex)


@db.command(name="json", help="Dump the database to JSON")
@click.pass_context
def db_json(context):
    """
    Dump database to JSON
    """
    import json

    """ Returns the entire content of a database as lists of dicts"""
    engine = context.obj["database"]
    meta = MetaData()
    # http://docs.sqlalchemy.org/en/rel_0_9/core/reflection.html
    meta.reflect(bind=engine)
    result = {}
    for table in meta.sorted_tables:
        result[table.name] = [dict(row) for row in engine.execute(table.select())]
    print(json.dumps(result, indent=4, default=str))


@db.command(name="init")
@click.option("-r", "--rls", is_flag=True, default=False, help="Row level security")
def db_init(rls):
    """
    Initialize database tables
    """
    import hashlib

    ini = home + "/pyfi.ini"

    try:
        from sqlalchemy import create_engine

        engine = None
        session = None

        try:
            _engine = create_engine(CONFIG.get("database", "uri"))
            _session = sessionmaker(bind=_engine)()
            users = _session.query(UserModel).all()
            print('Database already created. Please run "pyfi db drop".')
            _session.close()
            return
        except:
            pass

        try:
            engine = create_engine(POSTGRES_ROOT + "postgres")
            session = sessionmaker(bind=engine)()

            session.connection().connection.set_isolation_level(0)
            session.execute("CREATE DATABASE pyfi")
            session.connection().connection.set_isolation_level(1)
            print("Database created")
            session.close()
        except:
            pass

        try:
            engine = create_engine(CONFIG.get("database", "uri"))
            engine.uri = db
            session = sessionmaker(bind=engine)()
            session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            session.commit()
            # context.obj['database'] = engine
            # context.obj['session'] = session
            engine.session = session
        except:
            pass

        from pyfi.db.model import Base

        Base.metadata.create_all(engine)
        session.commit()

        try:
            sql = 'ALTER TABLE "user" ENABLE ROW LEVEL SECURITY'
            print("Enabling security on table user")
            session.execute(sql)
            session.commit()
            sql = 'CREATE POLICY user_security ON "user" USING (user.owner::text = current_user)'
            session.execute(sql)
            session.commit()
        except:
            pass

        try:
            sql = 'ALTER TABLE "login" ENABLE ROW LEVEL SECURITY'
            print("Enabling security on table login")
            session.execute(sql)
            session.commit()
            sql = 'CREATE POLICY user_security ON "login" USING (login.owner::text = current_user)'
            session.execute(sql)
            session.commit()
        except:
            pass

        session = sessionmaker(bind=engine)()

        if rls:
            for t in Base.metadata.sorted_tables:
                try:
                    sql = f'ALTER TABLE "{t.name}" ENABLE ROW LEVEL SECURITY'
                    print("Enabling security on table {}".format(t.name))
                    session.execute(sql)
                    session.commit()
                except Exception as ex:
                    print(ex)
                    session.rollback()

                try:
                    sql = f'CREATE POLICY {t.name}_security ON "{t.name}" USING ({t.name}.owner::text = current_user)'
                    print(sql)
                    session.execute(sql)
                    session.commit()
                except Exception as ex:
                    print(ex)
                    session.rollback()

        print("Database create all schemas done.")

        email = click.prompt("Postgres user email", type=str, default="p@e")
        password = click.prompt("Postgres user password", type=str, default="pyfi101")

        _password = hashlib.md5(password.encode()).hexdigest()

        if not CONFIG.has_section("login"):
            CONFIG.add_section("login")

        CONFIG.set("login", "password", _password)
        CONFIG.set("login", "user", "postgres")

        with open(ini, "w") as inifile:
            CONFIG.write(inifile)

        user = UserModel(
            name="postgres", email=email, password=_password, clear=password
        )
        role = RoleModel(name="admin")
        user.roles += [role]
        session.add(role)
        session.add(user)
        session.commit()
        session.close()
        print("Updated postgres user.")

    except Exception as ex:
        logging.error(ex)


@proc.command(name="remove")
@click.pass_context
def remove_processor(context):
    """
    Remove a processor
    """
    processor = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(id=context.obj["id"])
        .first()
    )
    # Business logic here?
    processor.requested_status = "removed"
    database = context.obj["database"]
    database.session.add(processor)
    database.session.commit()
    print("Processor remove requested.")


@proc.command(name="pause")
@click.option("-n", "--name", default=None, required=False)
@click.pass_context
def pause_processor(context, name):
    """
    Pause a processor
    """
    id = context.obj["id"]

    processor = None

    if name is not None:
        print("Pausing ", name)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        print("Pausing ", id)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

    # Business logic here?
    if processor:
        processor.requested_status = "paused"
        database = context.obj["database"]
        database.session.add(processor)
        database.session.commit()
        print("Processor pause requested.")
    else:
        print("Processor not found.")


@proc.command(name="resume")
@click.option("-n", "--name", default=None, required=False)
@click.pass_context
def resume_processor(context, name):
    """
    Pause a processor
    """
    id = context.obj["id"]

    processor = None
    if name is not None:
        print("Pausing ", name)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        print("Pausing ", id)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

    # Business logic here?
    if processor:
        processor.requested_status = "resumed"
        database = context.obj["database"]
        database.session.add(processor)
        database.session.commit()
        print("Processor resume requested.")
    else:
        print("Processor not found.")


@proc.command(name="stop")
@click.option("-n", "--name", default=None, required=False)
@click.pass_context
def stop_processor(context, name):
    """
    Stop a processor
    """
    id = context.obj["id"]

    processor = None
    if name is not None:
        print("Stopping", name)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        print("Stopping ", id)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

    # Business logic here?
    if processor:
        processor.requested_status = "stopped"
        database = context.obj["database"]
        database.session.add(processor)
        for deployment in processor.deployments:
            deployment.status = "stopped"
            database.session.add(deployment)

        database.session.commit()
        print("Processor stop requested.")
    else:
        print("Processor not found.")


@proc.command(name="start")
@click.option("-n", "--name", default=None, required=False)
@click.pass_context
def start_processor(context, name):
    """
    Start a processor
    """
    id = context.obj["id"]

    if name is not None:
        print("Starting", name)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        print("Starting", id)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

    # Business logic here?
    processor.requested_status = "start"
    database = context.obj["database"]
    database.session.add(processor)
    database.session.commit()
    print("Processor start requested.")


@proc.command(name="restart")
@click.option("-n", "--name", default=None, required=False)
@click.pass_context
def restart_processor(context, name):
    """
    Start a processor
    """
    id = context.obj["id"]

    if name is not None:
        print("Restarting", name)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        print("Restarting", id)
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

    # Business logic here?
    processor.requested_status = "restart"
    database = context.obj["database"]
    database.session.add(processor)
    database.session.commit()
    print("Processor restart requested.")


@cli.group()
@click.option("--id", default=None, help="ID of scheduler")
@click.option("-n", "--name", default=None, required=False, help="Name of scheduler")
@click.pass_context
def scheduler(context, id, name):
    """
    Scheduler management commands
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj["id"] = str(id)
    context.obj["name"] = name


@cli.group(name="delete")
def delete():
    """
    Delete an object from the database
    """
    pass


@delete.command(name="network", help="Delete a network")
@click.option("-n", "--name", default=None, help="Name of network")
@click.pass_context
def delete_network(context, name):
    network = (
        context.obj["database"].session.query(NetworkModel).filter_by(name=name).first()
    )
    context.obj["database"].session.delete(network)
    context.obj["database"].session.commit()
    print(f"Network {name} deleted.")


@delete.command(name="deployment", help="Delete a deployment")
@click.option("-n", "--name", default=None, help="Name of deployment")
@click.pass_context
def delete_deployment(context, name):
    deployment = (
        context.obj["database"]
        .session.query(DeploymentModel)
        .filter_by(name=name)
        .first()
    )

    if deployment.worker:
        deployment.worker.deployment = None
        context.obj["database"].session.commit()
    context.obj["database"].session.query(DeploymentModel).filter_by(name=name).delete()
    context.obj["database"].session.commit()
    print("Deployment deleted.")


@delete.command(name="calls", help="Delete all the call records")
@click.pass_context
def delete_calls(context):
    rows = context.obj["database"].session.query(CallModel).delete()
    print(rows, "deleted.")


@delete.command(name="socket", help="Delete a socket from the database")
@click.option(
    "-n", "--name", default=None, required=True, help="Name of socket being deleted"
)
@click.pass_context
def delete_socket(context, name):
    model = (
        context.obj["database"].session.query(SocketModel).filter_by(name=name).first()
    )

    context.obj["database"].session.delete(model)
    context.obj["database"].session.commit()


@delete.command(name="plug", help="Delete a plug from the database")
@click.option(
    "-n", "--name", default=None, required=True, help="Name of plug being deleted"
)
@click.pass_context
def delete_plug(context, name):
    model = (
        context.obj["database"].session.query(PlugModel).filter_by(name=name).first()
    )

    context.obj["database"].session.delete(model)
    context.obj["database"].session.commit()


@delete.command(name="task", help="Delete a task from the database")
@click.option(
    "-n", "--name", default=None, required=True, help="Name of task being deleted"
)
@click.pass_context
def delete_task(context, name):
    model = (
        context.obj["database"].session.query(TaskModel).filter_by(name=name).first()
    )

    context.obj["database"].session.delete(model)
    context.obj["database"].session.commit()


@delete.command(name="agent", help="Delete an agent from the database")
@click.option(
    "-n", "--name", default=None, required=True, help="Name of agent being deleted"
)
@click.pass_context
def delete_agent(context, name):
    model = (
        context.obj["database"].session.query(AgentModel).filter_by(name=name).first()
    )

    context.obj["database"].session.delete(model)
    context.obj["database"].session.commit()


@delete.command(name="processor", help="Delete a processor from the database")
@click.option(
    "-n", "--name", default=None, required=True, help="Name of processor being deleted"
)
@click.pass_context
def delete_processor(context, name):
    model = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(name=name)
        .first()
    )

    context.obj["database"].session.delete(model)
    context.obj["database"].session.commit()


@delete.command(name="user", help="Delete a user object from the database")
@click.option("--id", default=None, required=True, help="ID of user being deleted")
@click.pass_context
def delete_user(context, id):
    model = context.obj["database"].session.query(UserModel).filter_by(id=id).first()

    context.obj["database"].session.delete(model)
    context.obj["database"].session.commit()


@cli.group()
@click.option("--id", default=None, help="ID of object being added")
@click.pass_context
def add(context, id):
    """
    Add an object to the database
    """
    from uuid import uuid4

    if id is None:
        id = uuid4()

    context.obj["id"] = str(id)


@scheduler.command(name="start", help="Start the default scheduler")
@click.option("-n", "--name", default=None, required=True)
@click.option("-i", "--interval", default=3, required=False)
@click.option("-nd", "--nodeployments", default=False, is_flag=True, required=False)
@click.option(
    "-c", "--class", "clazz", default="pyfi.scheduler.BasicScheduler", required=False
)
@click.pass_context
def start_scheduler(context, name, interval, nodeployments, clazz):
    print("Starting scheduler {} with interval {} seconds.".format(name, interval))
    try:
        scheduler_class = import_class(clazz)
        scheduler = scheduler_class(name, nodeployments, interval)
        scheduler.run()
    except Exception as ex:
        logger.error(ex)
    # scheduler = BasicScheduler(name, interval)


@scheduler.command(name="remove")
@click.option(
    "-nd", "--node", default=None, required=False, help="Name of node to remove"
)
@click.pass_context
def remove_node_to_scheduler(context, node):
    """Remove node from scheduler"""
    pass


@scheduler.command(name="add")
@click.option("-nd", "--node", default=None, required=False, help="Name of node to add")
@click.pass_context
def add_node_to_scheduler(context, node):
    """
    Add a node to a scheduler
    """
    id = context.obj["id"]
    name = context.obj["name"]

    if name is not None:
        scheduler = (
            context.obj["database"]
            .session.query(SchedulerModel)
            .filter_by(name=name)
            .first()
        )

    elif id is not None:
        scheduler = (
            context.obj["database"]
            .session.query(SchedulerModel)
            .filter_by(id=id)
            .first()
        )

    if scheduler is None:
        print(f"Scheduler {name} does not exist.")
        return

    _node = (
        context.obj["database"].session.query(NodeModel).filter_by(name=node).first()
    )

    if _node is None:
        print(f"Node {node} does not exist.")
        return

    scheduler.nodes += [_node]

    context.obj["database"].session.add(scheduler)
    context.obj["database"].session.commit()

    print(_node)


@cli.group()
def task():
    """
    Pyfi task management
    """
    pass


@task.command(name="code", help="Print the task source code")
@click.option("-n", "--name", default=None, required=True, help="Name of task")
@click.pass_context
def code_task(context, name):
    import importlib
    import inspect

    task = context.obj["database"].session.query(TaskModel).filter_by(name=name).first()

    _code = task.code
    if _code is None:
        _module = importlib.import_module(task.module)
        _function = getattr(_module, task.name)
        _source = inspect.getsource(_function)
        print(_source)
    else:
        print(_code)


@task.command(name="show", help="Show details for a task")
@click.option("-n", "--name", required=True, help="Name of task to run")
@click.option("-g", "--gitrepo", is_flag=True, default=False)
@click.pass_context
def show_task(context, name, gitrepo):
    task = context.obj["database"].session.query(TaskModel).filter_by(name=name).first()

    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Module"]
    if gitrepo:
        names += ["Git Repo"]

    x.field_names = names

    nodes = [task]

    if task.code:
        print(task.code)

    for node in nodes:
        values = [node.name, node.id, node.owner, node.lastupdated, node.module]
        if gitrepo:
            values += [node.gitrepo]

        x.add_row(values)

    print(x)


@task.command(name="run")
@click.option("-n", "--name", required=False, help="Name of task to run")
@click.option(
    "-f",
    "--format",
    required=False,
    default="raw",
    help="Type of return data (json, pickle, raw)",
)
@click.option(
    "-s",
    "--socket",
    required=False,
    help="Name of socket associated with the task to run",
)
@click.option(
    "-d",
    "--data",
    required=False,
    help="Python evaluated string to pass to the socket's task",
)
@click.option(
    "-nd",
    "--nodata",
    required=False,
    is_flag=True,
    default=False,
    help="Set this flag if no data is being passed in.",
)
@click.option(
    "-a", "--argument", required=False, default=None, help="Name of argument to pass"
)
@click.option(
    "-sy",
    "--synchronized",
    is_flag=True,
    default=False,
    help="Execute full data flow from this task, wait for result.",
)
@click.pass_context
def run_task(context, name, format, socket, data, nodata, argument, synchronized):
    """
    Run a task
    """
    import imp
    import sys

    from pyfi.client.api import Socket, parallel, pipeline
    from pyfi.client.objects import SocketNotFoundException
    from pyfi.client.user import USER

    if socket is None:
        click.echo("No socket name was provided.")
        return

    _task = None

    if name:

        mymodule = imp.new_module(name)

        _task = (
            context.obj["database"]
            .session.query(TaskModel)
            .filter_by(name=name)
            .first()
        )

        if _task.code:
            result = exec(_task.code, mymodule.__dict__)

            if result:
                print(result)
            return

    user = context.obj["user"]
    socketname = socket
    try:
        socket = Socket(name=socketname, user=user, sync=synchronized)

        if socket is None:
            click.echo("Task must have code or socket connected.")
            return
    except SocketNotFoundException:
        click.echo(f"Socket {socketname} does not exist.")
        return

    kwargs = {}

    if synchronized:
        _data = None
        if data:
            if not argument:
                _args = eval(data)
                if type(_args) is list or type(_args) is tuple:
                    _data = [*eval(data)]
                else:
                    _data = eval(data)

        def build_pipeline(socket):

            sources = []
            for plug in socket.socket.sourceplugs:
                target_socket = plug.target
                _socket = Socket(name=target_socket.name, user=USER)
                pip = build_pipeline(_socket)
                if len(pip):
                    sources += [pipeline(_socket.p(), pip)]
                else:
                    sources += [_socket.p()]

            if len(sources) == 1:
                return sources[0]
            elif len(sources) > 1:
                return parallel(sources)
            else:
                return []

        p_calls = build_pipeline(socket)

        print("P_CALLS", p_calls)
        print("socket.p(_data).get() ", [socket.p(_data), p_calls])
        p = pipeline([socket.p(_data), p_calls])
        p = p_calls
        s1 = Socket(name="pyfi.processors.sample.do_something", user=USER).p
        s2 = Socket(name="pyfi.processors.sample.do_this", user=USER).p
        p = pipeline([s1("Hi!"), s2("There!")])
        print("PIPELINE", p)
        print(p().get())

        return

    if argument:
        found = False
        for _argument in _task.arguments:
            if _argument.name == argument:
                found = True
                break

        if not found:
            print("Argument {} not found.".format(argument))
            return

        o_argument = {
            "name": argument,
            "kind": _argument.kind,
            "key": socket.processor.name + "." + _task.module + "." + _task.name,
            "module": _task.module,
            "function": _task.name,
            "position": _argument.position,
        }

        kwargs["argument"] = o_argument

    if data:
        if not argument:
            _args = eval(data)
            if type(_args) is list or type(_args) is tuple:
                result = socket(*eval(data), **kwargs)
            else:
                result = socket(eval(data), **kwargs)
        else:
            result = socket(eval(data), **kwargs)
    elif nodata:
        result = socket(**kwargs)
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

        result = socket("".join(lines))

    # If type is set to pickle, then pickle the result
    # If type is set to json, then json dumps
    # otherwise type is 'raw', so print it
    print(result)


def update_object(obj, locals):
    """
    Docstring
    """
    for var in locals.keys():
        if locals[var] is not None and var != "id":
            setattr(obj, var, locals[var])

    obj.updated = datetime.now()

    return obj


@update.command(name="processor")
@click.option("-n", "--name", default=None, required=False)
@click.option("-m", "--module", default=None, required=False)
@click.option("-h", "--hostname", default=None, help="Target server hostname")
@click.option("-w", "--workers", default=None, help="Number of worker tasks")
@click.option("-g", "--gitrepo", default=None, help="Git repo URI")
@click.option("-c", "--commit", default=None, help="Git commit id for processor code")
@click.option("-b", "--beat", default=None, is_flag=True, required=False)
@click.option("-r", "--requested_status", default=None, required=False)
@click.option("-br", "--branch", default=None, required=False)
@click.option("-p", "--password", default=None, required=False)
@click.option("-co", "--container", default=None, is_flag=True, required=False)
@click.option("-mp", "--modulepath", default=None, required=False)
@click.pass_context
def update_processor(
    context,
    name,
    module,
    hostname,
    workers,
    gitrepo,
    commit,
    beat,
    requested_status,
    branch,
    password,
    container,
    modulepath,
):
    """
    Update a processor in the database
    """
    import inspect

    id = context.obj["id"] if "id" in context.obj else None

    if name is not None:
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )

    elif id is not None:
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

        # Update deployment

    if not module:
        processor.module = click.prompt("Module", type=str, default=processor.module)

    if not container:
        processor.use_container = click.prompt(
            "Container", type=bool, default=processor.use_container
        )

    if not workers:
        processor.concurrency = click.prompt(
            "Workers", type=int, default=processor.concurrency
        )

    if not gitrepo:
        processor.gitrepo = click.prompt("Gitrepo", type=str, default=processor.gitrepo)

    if not commit:
        processor.commit = click.prompt("Commit", type=str, default=processor.commit)

    if not branch:
        processor.branch = click.prompt("Branch", type=str, default=processor.branch)

    if not beat:
        processor.beat = click.prompt("Beat", type=bool, default=processor.beat)

    if not password:
        _password = click.prompt("Password", type=str, default=None)

        if _password:
            # Does password object exist first?

            __password = PasswordModel(
                name=processor.name + ".password", password=_password
            )
            context.obj["database"].session.add(__password)
            __password.processor = processor
    if not modulepath:
        processor.modulepath = click.prompt(
            "Module Path", type=str, default=processor.modulepath
        )
    argspec = inspect.getargvalues(inspect.currentframe())
    _locals = argspec.locals
    processor = update_object(processor, _locals)
    processor.requested_status = "update"
    context.obj["database"].session.add(processor)
    context.obj["database"].session.commit()


@add.command(name="log")
@click.option("-i", "--id", default=None, help="id of object")
@click.option("-s", "--source", default=None, required=False, help="Source name")
@click.option("-t", "--text", default=None, required=False, help="Text of log")
def add_log(context, id, source, text):
    """Add a log to the database"""
    pass


@add.command(name="argument")
@click.option(
    "-p", "--plug", prompt=True, required=True, default=None, help="Name of plug"
)
@click.option(
    "-t", "--task", prompt=True, required=True, default=None, help="Name of task"
)
@click.option(
    "-a",
    "--argument",
    prompt=True,
    required=True,
    default=None,
    help="Name of argument",
)
@click.pass_context
def add_argument(context, plug, task, argument):
    """Add argument to plug"""
    import importlib
    import inspect

    user = context.obj["user"]
    _task = (
        context.obj["database"].session.query(TaskModel).filter_by(name=task).first()
    )

    _plug = (
        context.obj["database"].session.query(PlugModel).filter_by(name=plug).first()
    )

    _module = importlib.import_module(_task.module)
    _function = getattr(_module, _task.name)

    signature = inspect.signature(_function)

    position = 0
    _task.arguments = []
    context.obj["database"].session.add(_task)
    context.obj["database"].session.add(_plug)
    for pname in signature.parameters:
        param = signature.parameters[pname]
        print("Name", param.name)
        print("Kind", param.kind)
        print("Default", param.default)
        _argument = ArgumentModel(
            name=param.name, position=position, user=user, kind=param.kind
        )
        _task.arguments += [_argument]
        position += 1

        if param.name == argument and _plug:
            context.obj["database"].session.add(_argument)
            logger.info("ADDING ARGUMENT")
            _plug.argument_id = _argument.id
            _argument.plugs += [_plug]
            # _plug.argument = _argument
            logger.info(
                "Added argument %s %s to plug %s", _plug.argument, _argument, _plug.name
            )

    _task.updated = datetime.now()
    context.obj["database"].session.commit()


@add.command(name="task")
@click.option(
    "-n", "--name", prompt=True, required=True, default=None, help="Name of this task"
)
@click.option(
    "-m",
    "--module",
    prompt=True,
    required=True,
    default=None,
    help="Python module (e.g. some.module.path",
)
@click.option(
    "-c", "--code", is_flag=True, default=None, help="Code flag. reads from stdin."
)
@click.option("-r", "--repo", default="None", help="Git repo containing packages")
@click.pass_context
def add_task(context, name, module, code, repo):
    """Add task to the database"""
    import importlib
    import inspect

    """
    Add task to the database
    """

    if code:
        # get from stdin
        code = sys.stdin.read()
        # exec(socket.task.code, module.__dict__)

    task = TaskModel(name=name, module=module, code=code, gitrepo=repo)

    context.obj["database"].session.add(task)
    _module = importlib.import_module(module)
    _function = getattr(_module, name)

    signature = inspect.signature(_function)

    position = 0
    for pname in signature.parameters:
        param = signature.parameters[pname]
        print("Name", param.name)
        print("Kind", param.kind)
        print("Default", param.default)
        argument = ArgumentModel(name=param.name, position=position, kind=param.kind)
        task.arguments += [argument]
        context.obj["database"].session.add(argument)
        position += 1
    # Create argument models from code and associate with task
    # task.arguments += [argument]

    task.updated = datetime.now()
    context.obj["database"].session.commit()

    print(task)


@add.command(name="deployment")
@click.option(
    "-n",
    "--name",
    prompt=True,
    required=True,
    default=None,
    help="Name of a processor",
)
@click.option(
    "-d",
    "--deploy",
    prompt=True,
    required=True,
    default=None,
    help="Name of this deployment",
)
@click.option("-h", "--hostname", default=None, help="Target server hostname")
@click.option("-c", "--cpus", default=0, help="Number of CPUs")
@click.pass_context
def add_deployment(context, name, deploy, hostname, cpus):
    """Add a deployment"""
    processor = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(name=name)
        .first()
    )

    deployment = (
        context.obj["database"]
        .session.query(DeploymentModel)
        .filter_by(name=deploy)
        .first()
    )

    if deployment is not None:
        logger.debug("Deployment {} exists.".format(deploy))
        return
    else:
        deployment = DeploymentModel(
            hostname=hostname, name=deploy, processor_id=processor.id, cpus=cpus
        )
        context.obj["database"].session.add(deployment)
        processor.deployments += [deployment]
        context.obj["database"].session.commit()
        logger.debug("Committed deployment")

    logger.debug("Deployment {}:{}:{} added.".format(deploy, hostname, cpus))


@add.command(name="processor")
@click.option(
    "-n",
    "--name",
    prompt=True,
    required=True,
    default=None,
    help="Name of this processor",
)
@click.option(
    "-m",
    "--module",
    prompt=True,
    required=True,
    default=None,
    help="Python module (e.g. some.module.path",
)
@click.option("-h", "--hostname", default=None, help="Target server hostname")
@click.option("-w", "--workers", default=1, help="Number of worker tasks")
@click.option(
    "-r", "--retries", default=5, help="Number of retries to invoke this processor"
)
@click.option(
    "-g", "--gitrepo", prompt=True, default=None, required=True, help="Git repo URI"
)
@click.option("-c", "--commit", default=None, help="Git commit id for processor code")
@click.option(
    "-rs",
    "--requested_status",
    default="ready",
    required=False,
    help="The requested status for this processor",
)
@click.option(
    "-b",
    "--beat",
    default=False,
    is_flag=True,
    required=False,
    help="Enable the beat scheduler",
)
@click.option(
    "-br",
    "--branch",
    default="main",
    required=False,
    help="Git branch to be used for checkouts",
)
@click.option(
    "-p",
    "--password",
    default=None,
    required=False,
    help="Password to access this processor",
)
@click.option(
    "-rq",
    "--requirements",
    default=None,
    required=False,
    help="requirements.txt file",
)
@click.option(
    "-e",
    "--endpoint",
    default=None,
    required=False,
    help="API endpoint path",
)
@click.option(
    "-a",
    "--api",
    default=True,
    required=False,
    help="Has an API endpoint",
)
@click.option(
    "-cs",
    "--cpus",
    default=-1,
    required=False,
    help="Number of CPUs for default deployment",
)
@click.option(
    "-d",
    "--deploy",
    default=False,
    is_flag=True,
    required=False,
    help="Enable the beat scheduler",
)
@click.option(
    "-mp",
    "--modulepath",
    default=None,
    required=False,
    help="Relative repo path to python module file",
)
@click.pass_context
def add_processor(
    context,
    name,
    module,
    hostname,
    workers,
    retries,
    gitrepo,
    commit,
    requested_status,
    beat,
    branch,
    password,
    requirements,
    endpoint,
    api,
    cpus,
    deploy,
    modulepath,
):
    """
    Add processor to the database
    """

    id = context.obj["id"]
    user = context.obj["user"]

    #  hostname=hostname,
    if endpoint is None:
        endpoint = "/" + module + "/" + name

    processor = ProcessorModel(
        id=id,
        status="ready",
        user_id=user.id,
        user=user,
        branch=branch,
        retries=retries,
        gitrepo=gitrepo,
        beat=beat,
        commit=commit,
        concurrency=workers,
        requested_status=requested_status,
        name=name,
        module=module,
        endpoint=endpoint,
        hasapi=api,
        requirements=requirements,
        modulepath=modulepath,
    )

    if password:
        _password = PasswordModel(
            name=name + ".password", password=hashlib.md5(password.encode()).hexdigest()
        )
        processor.password = _password

        context.obj["database"].session.add(_password)

    if deploy:
        if hostname and cpus > 0:
            deployment = DeploymentModel(
                name=processor.name, hostname=hostname, cpus=cpus
            )
            processor.deployments += [deployment]
            context.obj["database"].session.add(deployment)
        else:
            click.echo("Must provide hostname and CPUs > 0")
            return

    log1 = LogModel(
        oid=id,
        text="This is a log for " + name,
        user_id=user.id,
        public=True,
        user=user,
        discriminator="ProcessorModel",
        source="pyfi",
    )
    log2 = LogModel(
        oid=id,
        text="This is a log for " + name + " too",
        public=False,
        user_id=user.id,
        user=user,
        discriminator="ProcessorModel",
        source="pyfi",
    )

    context.obj["database"].session.add(log1)
    context.obj["database"].session.add(log2)

    processor.logs += [log1]
    processor.logs += [log2]
    processor.updated = datetime.now()

    context.obj["database"].session.add(processor)
    context.obj["database"].session.commit()

    print(processor)


@add.command(name="network")
@click.option("-n", "--name", default=None, required=True)
@click.pass_context
def add_network(context, name):
    """Create a named network"""

    user = context.obj["user"]
    network = NetworkModel(name=name, user=user)
    context.obj["database"].session.add(network)
    context.obj["database"].session.commit()
    print(f"Network {name} created.")


@add.command(name="privilege")
@click.option("-u", "--user", default=None, required=True)
@click.option("-n", "--name", default=None, required=True)
@click.option("-r", "--role", default=None, required=False)
@click.pass_context
def add_privilege(context, user, name, role):
    """
    Add privilege to the database
    """
    from sqlalchemy.exc import IntegrityError

    if user is None and role is None:
        print("User and Role cannot both be None.")
        return

    id = context.obj["id"]

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        try:
            user = (
                context.obj["database"]
                .session.query(UserModel)
                .filter_by(name=user)
                .first()
            )
            user.lastupdated = datetime.now()
            privilege = PrivilegeModel(id=id, name=name, right=name)
            user.privileges += [privilege]
            context.obj["database"].session.add(privilege)
            context.obj["database"].session.add(user)
            context.obj["database"].session.commit()
            print("Privilege added")
        except IntegrityError:
            import traceback

            print(traceback.format_exc())
            context.obj["database"].session.rollback()
            print("Error: Database constraint violation")


@add.command(name="user")
@click.option("-n", "--name", prompt=True, default=None, required=True)
@click.option("-e", "--email", prompt=True, default=None, required=True)
@click.option("-p", "--password", prompt=True, default=None, required=True)
@click.pass_context
def add_user(context, name, email, password):
    """
    Add user object to the database
    """
    import hashlib

    from sqlalchemy.exc import IntegrityError

    from pyfi.db.model import Base

    id = context.obj["id"]

    if name is None or email is None:
        raise click.UsageError("Name and Email are required")

    try:
        _password = hashlib.md5(password.encode()).hexdigest()
        # This user will be used in OSO authorizations
        user = UserModel(
            name=name, owner=name, password=_password, clear=password, email=email
        )
        user.lastupdated = datetime.now()

        context.obj["database"].session.add(user)
        context.obj["database"].session.commit()

        sql = f"CREATE USER {name} WITH PASSWORD '{password}'"
        print(sql)
        context.obj["database"].session.execute(sql)

        for t in Base.metadata.sorted_tables:
            sql = f'GRANT CONNECT ON DATABASE pyfi TO "{name}"'
            context.obj["database"].session.execute(sql)
            sql = f'GRANT SELECT, UPDATE, INSERT, DELETE ON "{t.name}" TO "{name}"'
            context.obj["database"].session.execute(sql)

        context.obj["database"].session.commit()
        print(f'User "{name}" added')
    except IntegrityError:
        import traceback

        print(traceback.format_exc())
        context.obj["database"].session.rollback()
        print("Error: Database constraint violation")


@add.command(name="scheduler")
@click.option("-n", "--name", required=True)
@click.option(
    "-s",
    "--strategy",
    type=click.Choice(["BALANCED", "EFFICIENT"]),
    default="BALANCED",
    required=False,
)
@click.pass_context
def add_scheduler(context, name, strategy):
    """
    Add scheduler object to the database
    """
    id = context.obj["id"]

    scheduler = SchedulerModel(name=name, strategy=strategy, id=id)
    scheduler.updated = datetime.now()
    context.obj["database"].session.add(scheduler)
    context.obj["database"].session.commit()

    print(scheduler)


@add.command(name="node")
@click.option("-n", "--name", required=True)
@click.option("-h", "--hostname", default=None, help="Hostname of the node")
@click.pass_context
def add_node(context, name, hostname):
    """
    Add node object to the database
    """
    id = context.obj["id"]

    node = NodeModel(name=name, id=id, hostname=hostname)
    node.updated = datetime.now()
    context.obj["database"].session.add(node)
    context.obj["database"].session.commit()

    print(node)


@add.command(name="agent")
@click.option("-n", "--name", required=True)
@click.option("-nd", "--node", required=True)
@click.pass_context
def add_agent(context, name, node):
    """
    Add agent object to the database
    """
    id = context.obj["id"]
    node = context.obj["database"].session.query(NodeModel).filter_by(name=node).first()

    agent = AgentModel(name=name, id=id, hostname=node.hostname, node_id=node.id)
    agent.updated = datetime.now()
    context.obj["database"].session.add(agent)
    context.obj["database"].session.commit()

    print(agent)


@add.command(name="role")
@click.option("-n", "--name", required=True)
@click.pass_context
def add_role(context, name):
    """
    Add role object to the database
    """
    id = context.obj["id"]

    role = RoleModel(name=name, id=id)
    role.updated = datetime.now()
    context.obj["database"].session.add(role)
    context.obj["database"].session.commit()

    print(role)


@add.command(name="queue")
@click.option("-n", "--name", required=True)
@click.option(
    "-t",
    "--type",
    type=click.Choice(["topic", "direct", "fanout"], case_sensitive=False),
    show_default=True,
    default="direct",
    required=True,
)
@click.pass_context
def add_queue(context, name, type):
    """
    Add queue object to the database
    """
    id = context.obj["id"]

    queue = QueueModel(
        name=name, id=id, qtype=type, requested_status="create", status="ready"
    )

    queue.updated = datetime.now()
    context.obj["database"].session.add(queue)
    context.obj["database"].session.commit()

    print(queue)


@update.command(name="task")
@click.option("-n", "--name", required=True)
@click.option("-m", "--module", is_flag=True, default=False)
@click.option(
    "-c", "--code", is_flag=True, default=None, help="Code flag. reads from stdin."
)
@click.pass_context
def update_task(context, name, module, code):
    """
    Update task in the database
    """

    if code:
        # get from stdin
        code = sys.stdin.read()

    _task = (
        context.obj["database"].session.query(TaskModel).filter_by(name=name).first()
    )

    if _task and code:
        _task.code = code
        _task.requested_status = "update"
        socket = (
            context.obj["database"]
            .session.query(SocketModel)
            .join(TaskModel)
            .filter(SocketModel.task_id == TaskModel.id)
            .first()
        )
        socket.processor.requested_status = "update"

        print(socket)

    context.obj["database"].session.add(_task)
    context.obj["database"].session.commit()


@update.command(name="socket")
@click.option("-n", "--name", required=True)
@click.option("-q", "--queue", default=None, help="Queue name")
@click.option("-i", "--interval", default=-1, required=False)
@click.option("-pi", "--procid", default=None, required=False, help="Processor id")
@click.option("-pn", "--procname", default=None, required=False, help="Processor name")
@click.option("-t", "--task", default=None, required=False, help="Task name")
@click.pass_context
def update_socket(context, name, queue, interval, procid, procname, task):
    """
    Update a socket in the database
    """

    # Get the named or id of the plug model
    if name is not None:
        socket = (
            context.obj["database"]
            .session.query(SocketModel)
            .filter_by(name=name)
            .first()
        )
    else:
        click.echo("Must provide socket name")
        return

    processor = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(id=socket.processor_id)
        .first()
    )
    if not interval and interval > 0:
        socket.interval = click.prompt("Interval", type=int, default=socket.interval)
        processor.requested_status = "update"

    if interval is not None:
        socket.interval = int(interval)

    context.obj["database"].session.commit()

    return


@update.command(name="plug")
@click.option("-n", "--name", required=True)
@click.option("-q", "--queue", required=True, help="Queue name")
@click.option("-pi", "--procid", default=None, required=False, help="Processor id")
@click.option("-pn", "--procname", default=None, required=False, help="Processor name")
@click.pass_context
def update_plug(context, name, queue, procid, procname):
    """
    Update or move a processor plug
    """
    import inspect

    id = context.obj["id"]

    # Get the named or id of the plug model
    if name is not None:
        plug = (
            context.obj["database"]
            .session.query(PlugModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        plug = context.obj["database"].session.query(PlugModel).filter_by(id=id).first()

    # Get the plug's current processor
    current_processor = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(id=plug.processor_id)
        .first()
    )

    # Get the processor referenced in the CLI
    if procname is not None:
        new_processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=procname)
            .first()
        )
    elif procid is not None:
        new_processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=procid)
            .first()
        )

    # If the new processor is different, then add it to the transaction
    # and request it be updated by the agent
    if new_processor.id != current_processor.id:
        new_processor.requested_status = "update"
        context.obj["database"].session.add(new_processor)

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
    current_processor.requested_status = "update"
    context.obj["database"].session.add(plug)
    context.obj["database"].session.add(current_processor)
    context.obj["database"].session.commit()
    print(plug)


@add.command(name="plug")
@click.option("-n", "--name", required=True)
@click.option("-q", "--queue", required=True, help="Queue name")
@click.option("-s", "--source", default=None, required=True, help="Source socket name")
@click.option("-t", "--target", default=None, required=True, help="Target socket name")
@click.pass_context
def add_plug(context, name, queue, source, target):
    """
    Add plug to a processor
    """
    id = context.obj["id"]

    source_socket = (
        context.obj["database"]
        .session.query(SocketModel)
        .filter_by(name=source)
        .first()
    )

    target_socket = (
        context.obj["database"]
        .session.query(SocketModel)
        .filter_by(name=target)
        .first()
    )

    queue = (
        context.obj["database"].session.query(QueueModel).filter_by(name=queue).first()
    )

    user = context.obj["user"]
    plug = PlugModel(
        name=name,
        id=id,
        requested_status="create",
        status="ready",
        processor=source_socket.processor,
        user=user,
        processor_id=source_socket.processor.id,
    )

    plug.source = source_socket
    plug.target = target_socket
    plug.queue = queue
    plug.updated = datetime.now()

    context.obj["database"].session.add(source_socket)
    context.obj["database"].session.add(target_socket)
    context.obj["database"].session.add(plug)
    context.obj["database"].session.commit()

    print(plug)


@add.command(name="socket")
@click.option("-n", "--name", required=True)
@click.option("-q", "--queue", required=True, help="Queue name")
@click.option(
    "-i",
    "--interval",
    default=10,
    required=False,
    help="Interval in seconds this socket is triggered",
)
@click.option("-pn", "--procname", default=None, required=True, help="Processor name")
@click.option("-t", "--task", default=None, required=True, help="Task name")
@click.pass_context
def add_socket(context, name, queue, interval, procname, task):
    """
    Add socket to a processor
    """
    id = context.obj["id"]

    processor = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(name=procname)
        .first()
    )

    queue = (
        context.obj["database"].session.query(QueueModel).filter_by(name=queue).first()
    )

    user = context.obj["user"]

    socket = SocketModel(
        name=name,
        id=id,
        user=user,
        user_id=user.id,
        requested_status="create",
        interval=interval,
        status="ready",
        processor_id=processor.id,
    )

    if task is not None:
        _task = (
            context.obj["database"]
            .session.query(TaskModel)
            .filter_by(name=task)
            .first()
        )
        if _task is None:
            _task = TaskModel(
                name=task, module=processor.module, gitrepo=processor.gitrepo
            )

            # Create Arguments and add to task

        socket.task = _task
        context.obj["database"].session.add(_task)

    socket.queue = queue
    socket.interval = interval
    socket.updated = datetime.now()
    processor.sockets += [socket]
    processor.requested_status = "update"
    context.obj["database"].session.add(socket)
    context.obj["database"].session.add(processor)
    context.obj["database"].session.commit()
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


@agent.command(name="kill")
@click.option("-n", "--name", required=True, help="Name of agent")
@click.pass_context
def kill_agent(context, name):
    """Kill an agent"""

    agent = (
        context.obj["database"].session.query(AgentModel).filter_by(name=name).first()
    )

    if not agent:
        print("Agent does not exist.")
        return

    agent.requested_status = "kill"
    context.obj["database"].session.commit()


@agent.command(name="stop")
@click.option("-n", "--name", required=True, help="Name of agent")
@click.pass_context
def stop_agent(context, name):
    """Stop an agent"""

    agent = (
        context.obj["database"].session.query(AgentModel).filter_by(name=name).first()
    )

    if not agent:
        print("Agent does not exist.")
        return

    agent.requested_status = "stop"
    context.obj["database"].session.commit()


@worker.command(name="kill", help="Kill a pyfi worker")
@click.option("-n", "--name", required=True, help="Name of worker")
@click.pass_context
def kill_worker(context, name):
    workerModel = (
        context.obj["database"].session.query(WorkerModel).filter_by(name=name).first()
    )
    workerModel.requested_status = "kill"

    context.obj["database"].session.commit()


@worker.command(name="start", help="Start a pyfi worker")
@click.option("-n", "--name", required=True, help="Name of worker")
@click.option("-a", "--agent", required=True, help="Name of agent")
@click.option("-h", "--hostname", required=True, help="Hostname to use")
@click.option("-p", "--pool", default=1, required=False, help="Size of worker pool")
@click.option(
    "-s",
    "--skip-venv",
    is_flag=True,
    default=False,
    required=False,
    help="Skip building the virtual environment",
)
@click.option(
    "-q",
    "--queue",
    default=1,
    help="Maximum number of messages on worker internal queue",
)
@click.pass_context
def start_worker(context, name, agent, hostname, pool, skip_venv, queue):
    from pyfi.worker import WorkerService

    agentModel = (
        context.obj["database"].session.query(AgentModel).filter_by(name=agent).first()
    )

    if agentModel is None:
        print("No agent by that name.")
        return

    workerModel = (
        context.obj["database"].session.query(WorkerModel).filter_by(name=name).first()
    )

    deployments = (
        context.obj["database"]
        .session.query(DeploymentModel)
        .filter_by(hostname=hostname)
        .all()
    )
    logging.debug("DEPLOYMENTS for %s are %s", hostname, deployments)

    for deployment in deployments:
        logging.debug("deployment.worker %s", deployment.worker)
        logging.debug("workerModel %s", workerModel)

        if deployment.worker is None and workerModel.deployment is None:
            logging.debug("Assigning deployment worker")
            deployment.worker = workerModel
            workerModel.deployment = deployment
            logging.debug("Adding deployment worker to session")
            context.obj["database"].session.add(deployment)
            context.obj["database"].session.add(workerModel)
            context.obj["database"].session.commit()
            context.obj["database"].session.flush()
            logging.debug("Committed session")
            logging.debug(
                "Assigned deployment %s to worker %s", deployment, workerModel
            )

    for deployment in deployments:
        """Just finding the the deployment for the current worker name"""
        logging.debug("deployment.worker %s", deployment.worker)
        logging.debug("workerModel %s", workerModel)

        if deployment.worker and deployment.worker.id == workerModel.id:
            logging.debug(
                "Assigning worker deployment based on ID %s", deployment.worker
            )
            workerModel.deployment = deployment
            break

        logger.debug(
            "Checking %s against worker.id %s", deployment.worker.id, workerModel.id
        )

    worker = {}
    processor = (
        context.obj["database"]
        .session.query(ProcessorModel)
        .filter_by(id=workerModel.processor_id)
        .first()
    )

    dir = "work/" + processor.id
    os.makedirs(dir, exist_ok=True)
    logger.debug("workerModel %s Deployment %s", workerModel, workerModel.deployment)

    if workerModel.deployment is None:
        logger.warning("This worker has no eligible deployments: %s", workerModel)
        return

    logger.debug("Creating WorkerService")
    try:
        context.obj["database"].session.expunge(processor)
        workerproc = WorkerService(
            processor,
            workdir=dir,
            basedir=os.getcwd(),
            hostname=hostname,
            deployment=workerModel.deployment,
            pool=pool,
            size=queue,
            database=context.obj["dburi"],
            skipvenv=skip_venv,
            celeryconfig=None,
            agent=agentModel,
            backend=CONFIG.get("backend", "uri"),
            broker=CONFIG.get("broker", "uri"),
        )
    except:
        logger.info("Error creating WorkerService")
        import traceback

        print(traceback.format_exc())
        return

    logger.debug("Creating WorkerService Done")
    logger.debug("FLOW WORKER START")
    wprocess = workerproc.start(start=True)

    workerModel.requested_status = "ready"
    workerModel.status = "running"
    context.obj["database"].session.add(workerModel)

    context.obj["database"].session.commit()
    wprocess.join()


@ls.command(name="passwords")
@click.pass_context
def ls_passwords(context):
    """List hashed passwords"""
    x = PrettyTable()

    names = [
        "Processor",
        "Hash",
        "Owner",
        "Last Updated",
    ]
    x.field_names = names
    passwords = context.obj["database"].session.query(PasswordModel).all()

    for node in passwords:
        print("PROC", node.processor)
        x.add_row([node.processor.name, node.password, node.owner, node.lastupdated])

    print(x)


@ls.command(name="queue")
@click.option("--id", default=None, help="ID of call")
@click.option("-n", "--name", default=None, required=False, help="Name of queue")
@click.option("-t", "--task", default=None, required=False, help="Name of task")
@click.pass_context
def ls_queue(context, id, name, task):
    """
    List a queue
    """
    import json

    # Combine info from database and rabbitmq about this queue
    import requests

    x = PrettyTable()
    if id is not None:
        queue = (
            context.obj["database"].session.query(QueueModel).filter_by(id=id).first()
        )
    elif name is not None:
        queue = (
            context.obj["database"]
            .session.query(QueueModel)
            .filter_by(name=name)
            .first()
        )

    if task:
        # Query for task, get task name, processor name and queue name
        # to combine into queuname.procname.taskname
        # Then return info about queuename and queuname.procname.taskname from broker
        pass

    user = CONFIG.get("broker", "user")
    password = CONFIG.get("broker", "password")
    uri = CONFIG.get("broker", "api")

    session = requests.Session()
    session.auth = (user, password)

    names = [
        "Name",
        "ID",
        "Owner",
        "Last Updated",
        "Messages",
        "Message TTL",
        "Expires",
        "Requested Status",
        "Broadcast Queue",
        "Status",
        "Type",
    ]

    x.field_names = names
    node = (
        context.obj["database"].session.query(QueueModel).filter_by(name=name).first()
    )

    messages = 0
    response = session.get(uri + "/queues/#/" + node.name)
    content = json.loads(response.content)
    for binding in content:
        if binding["name"].find(node.name) == 0:
            messages += binding["messages"]

    x.add_row(
        [
            node.name,
            node.id,
            node.owner,
            node.lastupdated,
            messages,
            node.message_ttl,
            node.expires,
            node.requested_status,
            node.name + ".topic",
            node.status,
            node.qtype,
        ]
    )

    print(x)

    x = PrettyTable()
    names = [
        "Name",
        "State",
        "Messages",
        "Rate",
        "Memory",
        "Durable",
        "Consumers",
        "Auto Delete",
    ]

    x.field_names = names
    for binding in content:
        if binding["name"] != "celery" and binding["name"].find(node.name) == 0:
            x.add_row(
                [
                    binding["name"],
                    binding["state"],
                    binding["messages"],
                    binding["messages_details"]["rate"],
                    binding["memory"],
                    binding["durable"],
                    binding["consumers"],
                    binding["auto_delete"],
                ]
            )

    print()
    print("Bindings")

    print(x)


@ls.command(name="call")
@click.option("--id", default=None, help="ID of call")
@click.option("-n", "--name", default=None, required=False, help="Name of call")
@click.option("-r", "--result", default=False, is_flag=True, help="Show result of call")
@click.option(
    "-t", "--tree", default=False, is_flag=True, help="Show forward call tree"
)
@click.option(
    "-g", "--graph", default=False, is_flag=True, help="Show complete call graph"
)
@click.option(
    "-f", "--flow", default=False, is_flag=True, help="Show all calls in a workflow"
)
@click.pass_context
def ls_call(context, id, name, result, tree, graph, flow):
    """
    List a call
    """
    import json

    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Last Updated",
        "Socket",
        "Started",
        "Finished",
        "State",
    ]
    x.field_names = names

    calls = None
    call = None

    if name is None and id is None:
        print("Must provide name or id. See $ pyfi ls call --help")
        return

    if name is not None:
        calls = (
            context.obj["database"].session.query(CallModel).filter_by(name=name).all()
        )
    elif id is not None:
        call = context.obj["database"].session.query(CallModel).filter_by(id=id).first()
        if call is None:
            print("No call with that id.")
            return
        if flow:  # task_id is NOT unique to each workflow invocation
            # Should use tracking
            nodes = (
                context.obj["database"]
                .session.query(CallModel)
                .filter_by(task_id=call.task_id)
                .all()
            )
        else:
            nodes = [call]

    if calls:
        nodes = calls
    elif call:
        import pickle

        if result:
            # TODO: Get from mongo

            from pymongo import MongoClient

            client = MongoClient(CONFIG.get("mongodb", "uri"))
            with client:
                db = client.celery
                result = db.celery_taskmeta.find_one(
                    {"_id": call.resultid.replace("celery-task-meta-", "")}
                )

                _r = pickle.loads(result["result"])

                if isinstance(_r, Exception):
                    import traceback

                    # _r = traceback.format_tb(_r.__traceback__)
                    print(_r.__traceback__)
                else:
                    try:
                        print(json.dumps(_r, indent=4))
                    except:
                        print(_r)
                return

        if graph:
            calls = (
                context.obj["database"]
                .session.query(CallModel)
                .filter_by(tracking=call.tracking)
                .all()
            )

            calldict = {}
            for _call in calls:
                calldict[call.celeryid] = _call

            from pptree import Node, print_tree

            for _call in calls:
                if _call.taskparent is None:
                    root = Node(_call.name)
                    break

            def get_call_graph(parent, node, _calls):
                logger.debug("node is %s", node)
                for _child in _calls:
                    logger.debug(
                        "_child %s %s %s %s",
                        _child.name,
                        _child.id,
                        _child.parent,
                        _child.task_id,
                    )
                    if _child.parent == node.id:
                        logger.debug("Found child node %s", _child)
                        _child_node = Node(_child.name, parent)
                        _child_node = get_call_graph(_child_node, _child, _calls)

                return parent

            _root = [_call for _call in calls if _call.parent is None][0]
            root = Node(_root.name)
            logger.debug("get_call_graph %s", call.tracking)
            root = get_call_graph(root, _root, calls)

            print_tree(root, horizontal=False)
            if not tree:
                return
        if tree:
            from pptree import Node, print_tree

            root = Node(call.name)

            def get_call_graph_root(root, _call):
                _calls = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .filter_by(parent=_call.id)
                    .all()
                )

                for _child in _calls:
                    _child_node = Node(_child.name, root)
                    _child_node = get_call_graph_root(_child_node, _child)

                return root

            root = get_call_graph_root(root, call)
            print_tree(root, horizontal=False)
            return

    for node in nodes:
        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.lastupdated,
                node.socket.name,
                node.started,
                node.finished,
                node.state,
            ]
        )
    print(x)
    x = PrettyTable()
    print()
    print("Function")
    names = ["ID", "Module", "Name"]
    x.field_names = names

    x.add_row([node.socket.task.id, node.socket.task.module, node.socket.task.name])
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
        print("Events")
        names = ["Name", "ID", "Owner", "Last Updated", "Note"]
        x.field_names = names
        if call:
            for call_event in call.events:
                x.add_row(
                    [
                        call_event.name,
                        call_event.id,
                        call_event.owner,
                        call_event.lastupdated,
                        call_event.note,
                    ]
                )
    print(x)


@ls.command(name="roles")
@click.option("-p", "--page", default=1, required=False)
@click.option("-r", "--rows", default=10, required=False)
@click.option("-a", "--ascend", default=False, is_flag=True, required=False)
@click.pass_context
def ls_roles(context, page, rows, ascend):
    """
    List roles
    """
    x = PrettyTable()

    names = ["Page", "Row", "Name", "ID", "Owner", "Last Updated", "Created"]
    x.field_names = names

    total = context.obj["database"].session.query(RoleModel).count()

    if total == 0:
        print(x)
        return

    if total > rows and page > round(total / rows):
        click.echo("Only {} pages exist.".format(round(total / rows)))
        return

    if not ascend:
        if total < rows:
            nodes = context.obj["database"].session.query(RoleModel).all()
        else:
            nodes = (
                context.obj["database"]
                .session.query(RoleModel)
                .order_by(RoleModel.lastupdated.desc())
                .offset((page - 1) * rows)
                .limit(rows)
            )
    else:
        if total < rows:
            nodes = context.obj["database"].session.query(RoleModel).all()
        else:
            nodes = (
                context.obj["database"]
                .session.query(RoleModel)
                .order_by(RoleModel.lastupdated.asc())
                .offset((page - 1) * rows)
                .limit(rows)
            )

    row = 0
    for node in nodes:
        row += 1
        x.add_row(
            [page, row, node.name, node.id, node.owner, node.lastupdated, node.created]
        )

    print(x)

    if total > 0:
        click.echo(
            "Page {} of {} of {} total records".format(page, round(total / rows), total)
        )
    else:
        click.echo("No rows")


@ls.command(name="jobs")
@click.option("-n", "--name", default=None, required=False, help="Name of processor")
@click.option("-p", "--page", default=1, required=False)
@click.option("-r", "--rows", default=10, required=False)
@click.option("-a", "--ascend", default=False, is_flag=True, required=False)
@click.pass_context
def ls_jobs(context, name, page, rows, ascend):
    """List scheduled jobs"""
    pass


@ls.command(name="job")
@click.pass_context
def ls_job(context, name, id):
    """List a job"""
    pass


@ls.command(name="calls")
@click.option("-p", "--page", default=1, required=False)
@click.option("-r", "--rows", default=10, required=False)
@click.option("-u", "--unfinished", is_flag=True, default=False, required=False)
@click.option("-a", "--ascend", default=False, is_flag=True, required=False)
@click.option("-i", "--id", is_flag=True, default=False, required=False)
@click.option("-t", "--tracking", is_flag=True, default=False, required=False)
@click.option("-tk", "--task", is_flag=True, default=False, required=False)
@click.pass_context
def ls_calls(context, page, rows, unfinished, ascend, id, tracking, task):
    """
    List calls
    """
    x = PrettyTable()

    names = ["Page", "Row", "Name"]

    if id:
        names += ["ID"]

    names += [
        "Queue",
        "Function",
        # "Task ID",
        # "Tracking",
        "Owner",
        "Last Updated",
        "Socket",
        "Started",
        "Finished",
        "State",
        "Argument",
    ]
    x.field_names = names

    if unfinished:
        total = (
            context.obj["database"]
            .session.query(CallModel)
            .filter_by(finished=None)
            .count()
        )
    else:
        total = context.obj["database"].session.query(CallModel).count()

    if total == 0:
        print(x)
        return

    if total > rows and page > round(total / rows):
        click.echo("Only {} pages exist.".format(round(total / rows)))
        return

    if not ascend:
        if total < rows:
            if unfinished:
                nodes = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .filter_by(finished=None)
                    .all()
                )
            else:
                nodes = context.obj["database"].session.query(CallModel).all()
        else:
            if unfinished:
                nodes = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .order_by(CallModel.lastupdated.desc())
                    .filter_by(finished=None)
                    .offset((page - 1) * rows)
                    .limit(rows)
                )
            else:
                nodes = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .order_by(CallModel.lastupdated.desc())
                    .offset((page - 1) * rows)
                    .limit(rows)
                )
    else:
        if total < rows:
            if unfinished:
                nodes = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .filter_by(finished=None)
                    .all()
                )
            else:
                nodes = context.obj["database"].session.query(CallModel).all()
        else:
            if unfinished:
                nodes = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .order_by(CallModel.lastupdated.asc())
                    .filter_by(finished=None)
                    .offset((page - 1) * rows)
                    .limit(rows)
                )
            else:
                nodes = (
                    context.obj["database"]
                    .session.query(CallModel)
                    .order_by(CallModel.lastupdated.asc())
                    .offset((page - 1) * rows)
                    .limit(rows)
                )

    row = 0
    for node in nodes:
        row += 1
        cols = [page, row, node.name]

        if id:
            cols += [node.id]

        cols += [
            node.socket.queue.name,
            node.socket.task.name,
            # node.resultid,
            # node.tracking,
            node.owner,
            node.lastupdated,
            node.socket.name,
            node.started,
            node.finished,
            node.state,
        ]

        if node.socket.task.arguments:
            cols += [node.argument]
        else:
            cols += [""]

        x.add_row(cols)

    print(x)

    if total > 0:
        click.echo(
            "Page {} of {} of {} total records".format(
                page, max(1, round(total / rows)), total
            )
        )
    else:
        click.echo("No rows")


@ls.command(name="network")
@click.option("-n", "--name", default=None, required=True, help="Name of network")
@click.option(
    "-h",
    "--horizontal",
    default=False,
    is_flag=True,
    required=False,
    help="Horizontal tree mode",
)
@click.option(
    "-v",
    "--vertical",
    default=False,
    is_flag=True,
    required=False,
    help="Vertical tree mode",
)
@click.pass_context
def ls_network(context, name, horizontal, vertical, condensed=True):
    """List the flow network"""

    from pptree import Node, print_tree

    if horizontal or vertical:
        condensed = False

    network = (
        context.obj["database"].session.query(NetworkModel).filter_by(name=name).first()
    )

    _root = Node("PYFI")
    root = Node(name, _root)
    if condensed:
        print("network::" + name)

    for node in network.nodes:
        node_node = Node("node::" + node.name, root)
        if condensed:
            print("  node::" + node.hostname)
        agent = node.agent
        if not agent:
            continue
        agent_node = Node("agent::" + agent.name, node_node)
        if condensed:
            print("    agent::" + agent.name)
        if not agent.workers:
            continue
        for worker in agent.workers:
            worker_node = Node("worker::" + worker.name, agent_node)
            if condensed:
                print("      worker::" + worker.name)
            processor_node = Node("processor::" + worker.processor.name, worker_node)
            if condensed:
                print("        processor::" + worker.processor.name)

            for socket in worker.processor.sockets:
                socket_node = Node("socket::" + socket.name, processor_node)
                if condensed:
                    print("          socket::" + socket.name)
                task_node = Node("task::" + socket.task.name, socket_node)
                if condensed:
                    print("            task::" + socket.task.name)
                module_node = Node("module::" + socket.task.module, task_node)
                if condensed:
                    print("              module::" + socket.task.module)
                function_node = Node("function::" + socket.task.name, task_node)
                if condensed:
                    print("                 function::" + socket.task.name)
                for plug in socket.sourceplugs:
                    plug_node = Node("plug::" + plug.name)
                    if condensed:
                        print("                      plug::" + plug.name)

                    source_node = Node("source::" + plug.source.name)
                    if condensed:
                        print("                        source::" + plug.source.name)
                        print("                        target::" + plug.target.name)

                for arg in socket.task.arguments:
                    argument_node = Node("argument::" + arg.name, function_node)
                    if condensed:
                        print("                    argument::" + arg.name)

                    for plug in arg.plugs:
                        plug_node = Node("plug::" + plug.name)
                        if condensed:
                            print("                      plug::" + plug.name)

                        source_node = Node("source::" + plug.source.name)
                        if condensed:
                            print("                        source::" + plug.source.name)
                            print("                        target::" + plug.target.name)

    if not condensed:
        print_tree(root, horizontal=horizontal)


@ls.command(name="work")
@click.pass_context
def ls_work(context):
    """
    List work
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


@ls.command(name="worker")
@click.pass_context
def ls_worker(context):
    """
    List a worker
    """
    pass


@ls.command(name="socket")
@click.option("--id", default=None, help="ID of call")
@click.option("-n", "--name", default=None, required=False, help="Name of call")
@click.option(
    "-g", "--graph", default=False, is_flag=True, help="Show complete call graph"
)
@click.pass_context
def ls_socket(context, id, name, graph):
    """
    List a socket
    """
    sockets = []
    socket = None

    if name is not None:
        socket = (
            context.obj["database"]
            .session.query(SocketModel)
            .filter_by(name=name)
            .first()
        )
        sockets = [socket]
    elif id is not None:
        socket = (
            context.obj["database"].session.query(SocketModel).filter_by(id=id).first()
        )
        sockets = [socket]

    if not socket:
        click.echo("No socket was found")
        return

    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Module",
        "Task",
        "Last Updated",
        "Status",
        "Processor",
        "Queue",
        "Interval",
    ]

    x.field_names = names

    for node in sockets:
        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.task.module,
                node.task.name,
                node.lastupdated,
                node.status,
                node.processor.name,
                node.queue.name,
                node.interval,
            ]
        )

    from pptree import Node, print_tree

    # TODO: Add graph for outbound plugs of this socket

    root = Node(socket.name)
    module = Node(socket.task.module, root)
    task = Node(socket.task.name, module)

    if graph:
        print_tree(root, horizontal=False)
    else:
        print(x)

    # Print plugs


@ls.command(name="scheduler")
@click.pass_context
def ls_scheduler(context):
    """
    List a scheduler
    """
    pass


@ls.command(name="processor")
@click.option("--id", default=None, help="ID of call")
@click.option("-n", "--name", default=None, required=False, help="Name of call")
@click.option(
    "-g", "--graph", default=False, is_flag=True, help="Show complete call graph"
)
@click.pass_context
def ls_processor(context, id, name, graph):
    """
    List a processor
    """
    from pptree import Node, print_tree

    if name is not None:
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(name=name)
            .first()
        )
    elif id is not None:
        processor = (
            context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(id=id)
            .first()
        )

    if processor is None:
        print("No processor found.")
        return

    sockets = processor.sockets
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Module",
        "Task",
        "Last Updated",
        "Status",
        "Processor",
        "Queue",
        "Interval",
    ]

    x.field_names = names

    root = Node(processor.name)
    for node in sockets:
        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.task.module,
                node.task.name,
                node.lastupdated,
                node.status,
                node.processor.name,
                node.queue.name,
                node.interval,
            ]
        )

        sock = Node(node.name, root)
        module = Node(node.task.module, sock)
        task = Node(node.task.name, module)

    if graph:
        print_tree(root, horizontal=False)
    else:
        print("Name:", processor.name)
        print("ID:", processor.id)
        print("Module:", processor.module)
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

    nodes = processor.deployments
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Last Updated",
        "Hostname",
        "Processor",
        "CPUs",
        "Requested Status",
        "Status",
        "Enabled",
    ]
    x.field_names = names
    nodes = (
        context.obj["database"]
        .session.query(DeploymentModel)
        .filter_by(processor_id=processor.id)
        .all()
    )
    for node in nodes:
        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.lastupdated,
                node.hostname,
                node.processor.name,
                node.cpus,
                node.requested_status,
                node.status,
                "TBD",
            ]
        )

    print()
    print("Deployments")
    print(x)


@ls.command(name="task")
@click.option("-n", "--name", default=None, required=True, help="Name of task")
@click.option(
    "-s", "--source", is_flag=True, required=False, help="Source of task function"
)
@click.option(
    "-c", "--code", is_flag=True, required=False, help="Code override of task"
)
@click.option(
    "-p", "--plugs", is_flag=True, default=False, required=False, help="Show plugs"
)
@click.option(
    "-so", "--sockets", is_flag=True, default=False, required=False, help="Show sockets"
)
@click.pass_context
def ls_task(context, name, source, code, plugs, sockets):
    """
    List a task
    """

    task = context.obj["database"].session.query(TaskModel).filter_by(name=name).first()

    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Module"]
    names += ["Git Repo"]
    x.field_names = names
    tasks = [task]

    if source:
        print(task.source)
        return
    if code:
        print(task.code)
        return

    node = None

    for node in tasks:
        values = [node.name, node.id, node.owner, node.lastupdated, node.module]

        values += [node.gitrepo]
        x.add_row(values)

    print(x)
    print()

    print("Arguments")
    x = PrettyTable()

    names = ["ID", "Name", "Module", "Position", "Kind", "Function"]
    x.field_names = names

    kinds = [
        "POSITIONAL_ONLY",
        "POSITIONAL_OR_KEYWORD",
        "VAR_POSITIONAL",
        "KEYWORD_ONLY",
        "VAR_KEYWORD",
    ]
    for arg in node.arguments:
        values = [
            arg.id,
            arg.name,
            task.module,
            arg.position,
            kinds[int(arg.kind)],
            task.name,
        ]

        x.add_row(values)

    print(x)

    if sockets:
        print()
        print("Sockets")
        x = PrettyTable()
        names = [
            "Name",
            "ID",
            "Owner",
            "Module",
            "Task",
            "Last Updated",
            "Status",
            "Processor",
            "Queue",
            "Interval",
        ]

        x.field_names = names

        for node in task.sockets:
            x.add_row(
                [
                    node.name,
                    node.id,
                    node.owner,
                    node.task.module,
                    node.task.name,
                    node.lastupdated,
                    node.status,
                    node.processor.name,
                    node.queue.name,
                    node.interval,
                ]
            )

        print(x)

    if plugs:

        print()
        print("Plugs")

        x = PrettyTable()

        names = [
            "Name",
            "ID",
            "Type",
            "Owner",
            "Last Updated",
            "Status",
            "Processor",
            "Queue",
            "Source",
            "Target",
        ]
        x.field_names = names
        plugs = context.obj["database"].session.query(PlugModel).all()

        for socket in task.sockets:
            for node in socket.sourceplugs:
                x.add_row(
                    [
                        node.name,
                        node.id,
                        node.type,
                        node.owner,
                        node.lastupdated,
                        node.status,
                        node.processor.name,
                        node.queue.name,
                        node.source.name,
                        node.target.name,
                    ]
                )
            for node in socket.targetplugs:
                x.add_row(
                    [
                        node.name,
                        node.id,
                        node.type,
                        node.owner,
                        node.lastupdated,
                        node.status,
                        node.processor.name,
                        node.queue.name,
                        node.source.name,
                        node.target.name,
                    ]
                )

        print(x)


@ls.command(name="stats")
@click.pass_context
def ls_stats(context):
    """
    List object stats
    """
    pass


@ls.command(name="deployments")
@click.pass_context
def ls_deployments(context):
    """
    List deployments
    """
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Worker",
        "Last Updated",
        "Hostname",
        "Processor",
        "CPUs",
        "Requested Status",
        "Status",
        "Enabled",
    ]
    x.field_names = names
    deployments = context.obj["database"].session.query(DeploymentModel).all()
    for deployment in deployments:
        x.add_row(
            [
                deployment.name,
                deployment.id,
                deployment.owner,
                deployment.worker.name if deployment.worker else "pending",
                deployment.lastupdated,
                deployment.hostname,
                deployment.processor.name,
                deployment.cpus,
                deployment.requested_status,
                deployment.status,
                "TBD",
            ]
        )

    print(x)


@ls.command(name="schedulers")
@click.pass_context
def ls_schedulers(context):
    """
    List schedulers
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Strategy", "Nodes"]
    x.field_names = names
    nodes = context.obj["database"].session.query(SchedulerModel).all()
    for node in nodes:
        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.lastupdated,
                node.strategy,
                [n.name for n in node.nodes],
            ]
        )

    print(x)


@ls.command(name="networks")
@click.pass_context
def ls_networks(context):
    """List current networks"""
    x = PrettyTable()

    names = ["Name", "ID"]
    x.field_names = names
    nodes = context.obj["database"].session.query(NetworkModel).all()
    for node in nodes:
        x.add_row([node.name, node.id])

    print(x)


@ls.command(name="nodes")
@click.pass_context
def ls_nodes(context):
    """
    List nodes
    """
    import humanize

    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Host",
        "Network",
        "Owner",
        "Last Updated",
        "CPUs",
        "Load",
        "Mem Size",
        "Free Mem",
        "Used Mem",
        "Agent",
    ]
    x.field_names = names
    nodes = context.obj["database"].session.query(NodeModel).all()
    for node in nodes:
        if node.network:
            network = node.network.name
        else:
            network = "None"
        agent_name = node.agent.name if node.agent else "None"
        x.add_row(
            [
                node.name,
                node.id,
                node.hostname,
                network,
                node.owner,
                node.lastupdated,
                node.cpus,
                node.cpuload,
                humanize.naturalsize(node.memsize, gnu=True),
                "{:.2f}%".format(round(float(node.freemem), 2)),
                "{:.2f}%".format(round(float(node.memused), 2)),
                agent_name,
            ]
        )

    print(x)


@ls.command(name="queues")
@click.pass_context
def ls_queues(context):
    """
    List queues
    """
    import json

    import requests

    x = PrettyTable()

    uri = CONFIG.get("broker", "api")
    user = CONFIG.get("broker", "user")
    pwd = CONFIG.get("broker", "password")
    session = requests.Session()
    session.auth = (user, pwd)

    session.post(uri)

    names = [
        "Name",
        "ID",
        "Owner",
        "Last Updated",
        "Messages",
        "Message TTL",
        "Expires",
        "Requested Status",
        "Broadcast Queue",
        "Status",
        "Type",
    ]

    x.field_names = names
    queues = context.obj["database"].session.query(QueueModel).all()

    for node in queues:
        messages = 0
        try:
            response = session.get(uri + "/queues/#/" + node.name)
            content = json.loads(response.content)
            for binding in content:
                if binding["name"].find(node.name) == 0:
                    messages += binding["messages"]
        except:
            pass

        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.lastupdated,
                messages,
                node.message_ttl,
                node.expires,
                node.requested_status,
                node.name + ".topic",
                node.status,
                node.qtype,
            ]
        )

    print(x)


@ls.command(name="users")
@click.pass_context
def ls_users(context):
    """
    List users
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Email", "Password"]
    x.field_names = names

    context.obj["database"].session.execute("select current_user").first()
    users = context.obj["database"].session.query(UserModel).all()
    for user in users:
        x.add_row([user.name, user.id, user.owner, user.email, user.password])

    print(x)


@ls.command(name="role")
@click.option("-n", "--name", default=None, required=True)
@click.pass_context
def ls_role(context, name):
    """List a role"""
    import warnings

    x = PrettyTable()
    names = ["Name", "Last Updated", "By"]
    x.field_names = names

    roles = []

    role = context.obj["database"].session.query(RoleModel).filter_by(name=name).first()

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


@ls.command(name="user")
@click.option("-n", "--name", default=None, required=True)
@click.pass_context
def ls_user(context, name):
    """
    List a user
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Email"]
    x.field_names = names
    user = context.obj["database"].session.query(UserModel).filter_by(name=name).first()
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


@ls.command(name="workers")
@click.option(
    "-n",
    "--name",
    default=False,
    is_flag=True,
    required=False,
    help="List worker names",
)
@click.pass_context
def ls_workers(context, name):
    """
    List workers
    """
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Port",
        "Process",
        "Last Updated",
        "Requested Status",
        "Status",
        "Agent",
        "Backend",
        "Broker",
        "Hostname",
        "Processor",
        "Concurrency",
        "Deployment",
        "Workdir",
    ]
    x.field_names = names
    workers = context.obj["database"].session.query(WorkerModel).all()

    for node in workers:
        if node.processor is None:
            pname = "None"
        else:
            pname = node.processor.name

        hostname = node.deployment.hostname if node.deployment else "None"
        _name = node.deployment.name if node.deployment else "None"

        if name:
            click.echo(node.name)

        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.port,
                node.process,
                node.lastupdated,
                node.requested_status,
                node.status,
                node.agent.name,
                node.backend,
                node.broker,
                hostname,
                pname,
                node.concurrency,
                _name,
                node.workerdir,
            ]
        )

    if not name:
        print(x)


@ls.command(name="processors")
@click.option("-g", "--gitrepo", is_flag=True, default=False)
@click.option("-c", "--commit", is_flag=True, default=False)
@click.option("-m", "--module", is_flag=True, default=False)
@click.option("-o", "--owner", is_flag=True, default=False)
@click.pass_context
def ls_processors(context, gitrepo, commit, module, owner):
    """
    List processors
    """
    processors = context.obj["database"].session.query(ProcessorModel).all()
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Module",
        "Owner",
        "Last Updated",
        "Requested Status",
        "Status",
        "Concurrency",
        "Deployed CPUs",
        "Beat",
        "Sockets",
    ]

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
        deployed_cpus = 0
        for deployment in processor.deployments:
            deployed_cpus += deployment.cpus
        row = [
            processor.name,
            processor.id,
            processor.module,
            processor.owner,
            processor.lastupdated,
            processor.requested_status,
            processor.status,
            processor.concurrency,
            deployed_cpus,
            processor.beat,
            len(processor.sockets),
        ]

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


@ls.command(name="tasks")
@click.option("-g", "--gitrepo", is_flag=True, default=False)
@click.pass_context
def ls_tasks(context, gitrepo):
    """
    List tasks
    """
    x = PrettyTable()

    names = ["Name", "ID", "Owner", "Last Updated", "Module"]
    if gitrepo:
        names += ["Git Repo"]
    x.field_names = names
    tasks = context.obj["database"].session.query(TaskModel).all()

    for node in tasks:
        values = [node.name, node.id, node.owner, node.lastupdated, node.module]

        if gitrepo:
            values += [node.gitrepo]
        x.add_row(values)

    print(x)


@ls.command(name="cpus")
@click.pass_context
def ls_cpus(context):
    """
    List network cpus
    """
    pass


@ls.command(name="agent")
@click.pass_context
def ls_agent(context):
    """
    List an agent
    """
    pass


@ls.command(name="agents")
@click.pass_context
def ls_agents(context):
    """
    List agents
    """

    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Host",
        "CPUs",
        "Port",
        "Owner",
        "Last Updated",
        "Requested Status",
        "Status",
        "Node",
        "PID",
    ]
    x.field_names = names
    agents = context.obj["database"].session.query(AgentModel).all()

    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sa_exc.SAWarning)
        for node in agents:
            # worker_name = node.worker.name if node.worker else 'None'
            x.add_row(
                [
                    node.name,
                    node.id,
                    node.hostname,
                    node.cpus,
                    node.port,
                    node.owner,
                    node.lastupdated,
                    node.requested_status,
                    node.status,
                    node.node.name,
                    node.pid,
                ]
            )

    print(x)


@ls.command(name="sockets")
@click.pass_context
def ls_sockets(context):
    """
    List sockets
    """
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Owner",
        "Module",
        "Task",
        "Last Updated",
        "Status",
        "Processor",
        "Queue",
        "Type",
        "Interval",
    ]
    x.field_names = names
    sockets = context.obj["database"].session.query(SocketModel).all()

    for node in sockets:
        x.add_row(
            [
                node.name,
                node.id,
                node.owner,
                node.task.module,
                node.task.name,
                node.lastupdated,
                node.status,
                node.processor.name,
                node.queue.name,
                node.schedule_type,
                node.interval,
            ]
        )

    print(x)


@ls.command(name="node")
@click.option("-n", "--name", default=None, required=True, help="Name of node")
@click.option(
    "-t",
    "--tree",
    default=False,
    is_flag=True,
    required=False,
    help="Display object tree",
)
@click.option(
    "-h",
    "--horizontal",
    default=True,
    is_flag=True,
    required=False,
    help="Vertical tree mode",
)
@click.pass_context
def ls_node(context, name, tree, horizontal):
    """
    List a node
    """
    from pptree import Node, print_tree

    node = context.obj["database"].session.query(NodeModel).filter_by(name=name).first()

    if not node:
        return

    if tree:
        root = Node("node::" + node.name)
        agent = Node("agent::" + node.agent.name, root)
        for _worker in node.agent.workers:
            worker = Node("worker::" + _worker.name, agent)
            processor = Node("processor::" + _worker.processor.name, worker)

            for socket in _worker.processor.sockets:
                _sock = Node("socket::" + socket.name, processor)
                Node("task::" + socket.task.name, _sock)

        print_tree(root, horizontal=not horizontal)


@ls.command(name="plug")
@click.option("-n", "--name", default=None, required=True, help="Name of processor")
@click.pass_context
def ls_plug(context, name):
    """
    List a plug
    """
    x = PrettyTable()

    plug = context.obj["database"].session.query(PlugModel).filter_by(name=name).first()

    names = [
        "Name",
        "ID",
        "Owner",
        "Last Updated",
        "Status",
        "Queue",
        "Source Task",
        "Target Task",
        "Source Socket",
        "Target Socket",
    ]
    x.field_names = names

    node = plug
    x.add_row(
        [
            node.name,
            node.id,
            node.owner,
            node.lastupdated,
            node.status,
            node.queue.name,
            node.source.task.name,
            node.target.task.name,
            node.source.name,
            node.target.name,
        ]
    )

    print(x)
    print()
    print("Source Task")
    x = PrettyTable()

    names = ["ID", "Name", "Module"]
    x.field_names = names

    for task in [plug.source.task]:
        values = [task.id, task.name, task.module]

        x.add_row(values)

    print(x)
    print()

    print("Target Task")
    x = PrettyTable()

    names = ["ID", "Name", "Module"]
    x.field_names = names

    for task in [plug.target.task]:
        values = [task.id, task.name, task.module]

        x.add_row(values)

    print(x)
    print()

    print("Argument")

    x = PrettyTable()

    names = ["ID", "Name", "Task", "Module", "Position", "Kind", "Function"]
    x.field_names = names

    kinds = [
        "POSITIONAL_ONLY",
        "POSITIONAL_OR_KEYWORD",
        "VAR_POSITIONAL",
        "KEYWORD_ONLY",
        "VAR_KEYWORD",
    ]
    for arg in [plug.argument]:
        if arg:
            values = [
                arg.id,
                arg.name,
                arg.task.id,
                arg.task.module,
                arg.position,
                kinds[int(arg.kind)],
                arg.task.name,
            ]

            x.add_row(values)

    print(x)


@ls.command(name="plugs")
@click.pass_context
def ls_plugs(context):
    """
    List plugs
    """
    x = PrettyTable()

    names = [
        "Name",
        "ID",
        "Type",
        "Owner",
        "Last Updated",
        "Status",
        "Processor",
        "Queue",
        "Source",
        "Target",
    ]
    x.field_names = names
    plugs = context.obj["database"].session.query(PlugModel).all()

    for node in plugs:
        x.add_row(
            [
                node.name,
                node.id,
                node.type,
                node.owner,
                node.lastupdated,
                node.status,
                node.processor.name,
                node.queue.name,
                node.source.name,
                node.target.name,
            ]
        )

    print(x)


@cli.command(help="Listen to a processor output")
@click.option("-n", "--name", default=None, required=True, help="Name of processor")
@click.option(
    "-c",
    "--channel",
    default="task",
    required=True,
    help="Listen channel (e.g. task, log, etc)",
)
@click.option(
    "-a",
    "--adaptor",
    default=None,
    help="Adaptor class function (e.g. my.module.class.function)",
)
@click.pass_context
def listen(context, name, channel, adaptor):
    """
    Listen on a pub/sub channel
    """
    import importlib

    import redis

    redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))
    p = redisclient.pubsub()
    p.psubscribe([name + "." + channel])
    print("Listening to", name)
    func = None
    if adaptor:
        module = importlib.import_module(".".join(adaptor.rsplit(".")[:-1]))
        _class = getattr(module, adaptor.rsplit(".")[-1:][0])
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
    name = context.obj["user"].name if context.obj["user"] is not None else None

    loginstr = "Not logged in"
    if name is not None:
        loginstr = "Logged into flow as " + name
    print("Database user {}.\n{}.".format(context.obj["owner"], loginstr))


@cli.group()
def api():
    """
    API server admin
    """
    pass


@api.command(name="start")
@click.option("-ip", default="0.0.0.0", help="IP bind address")
@click.option("-p", "--port", default=8000, help="Listen port")
@click.pass_context
def api_start(context, ip, port):
    """
    Run pyfi API server
    """
    import multiprocessing

    import bjoern
    import gunicorn.app.base

    from pyfi.api import blueprint
    from pyfi.server.api import app as server
    from pyfi.server.api import create_endpoint

    """ Spawn this as a managed sub process. """

    def start_api():
        cpus = multiprocessing.cpu_count()

        class StandaloneApplication(gunicorn.app.base.BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()
                print("GUNICORN APP START")

            def load_config(self):
                config = {
                    key: value
                    for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None
                }
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        logger.info("Initializing server app....")
        logger.info("Serving API on {}:{}".format(ip, port))

        server.register_blueprint(blueprint)

        """
        do_something = context.obj["database"].session.query(TaskModel).filter_by(name='do_something').first()
        do_this = context.obj["database"].session.query(TaskModel).filter_by(name='do_this').first()

        if do_something:
            create_endpoint(do_something.module,do_something.name)

        if do_this:
            create_endpoint(do_this.module,do_this.name)
        """

        tasks = context.obj["database"].session.query(TaskModel).all()

        for task in tasks:
            create_endpoint(task.module, task.name)

        server.app_context().push()

        try:
            """
            options = {
                "bind": "%s:%s" % ("0.0.0.0", str(port)),
                "workers": cpus,
                # 'threads': number_of_workers(),
                "timeout": 120,
            }
            StandaloneApplication(server, options).run()
            """
            bjoern.run(server, ip, port)
        except Exception as ex:
            logging.error(ex)
            logger.info("Shutting down...")

    cont = True
    while cont:
        import signal
        import time

        def handler(signum, fram):
            exit(0)

        signal.signal(signal.SIGINT, handler)

        process = multiprocessing.Process(target=start_api)
        click.echo("Starting API process.")
        process.start()
        click.echo("API process started.")
        process.join()
        time.sleep(15)
        click.echo("Terminating API server and restarting...")
        process.terminate()

    click.echo("API process exited.")


@agent.command(name="start")
@click.option("-p", "--port", default=8001, help="Healthcheck port")
@click.option(
    "--clean", default=False, is_flag=True, help="Remove work directories before launch"
)
@click.option(
    "-b", "--backend", default="redis://localhost", help="Message backend URI"
)
@click.option("-r", "--broker", default="pyamqp://localhost", help="Message broker URI")
@click.option("-n", "--name", default=None, help="Hostname for this agent to use")
@click.option(
    "-c",
    "--config",
    default=None,
    help="Config module.object import (e.g. path.to.module.MyConfigClass",
)
@click.option("-q", "--queues", is_flag=True, help="Run the queue monitor only")
@click.option("-u", "--user", default=None, help="Run the worker as user")
@click.option("-po", "--pool", default=1, help="Process pool for message dispatches")
@click.option("-cp", "--cpus", default=-1, help="Number of CPUs")
@click.option(
    "-s",
    "--size",
    default=10,
    help="Maximum number of messages on worker internal queue",
)
@click.option("-h", "--host", help="Remote hostname to start the agent via ssh")
@click.option("-wp", "--workerport", default=-1, help="Healthcheck port for worker")
@click.pass_context
def start_agent(
    context,
    port,
    clean,
    backend,
    broker,
    name,
    config,
    queues,
    user,
    pool,
    cpus,
    size,
    host,
    workerport,
):
    """
    Start an agent
    """
    from pyfi.agent import AgentService

    logger.info("start_agent name is %s cpus %s", name, cpus)
    if name:
        os.environ["PYFI_HOSTNAME"] = name
    else:
        name = "localhost"

    if host is not None:
        logger.debug("host is %s", host)
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

        if CONFIG.has_section("services"):
            agent_class_name = CONFIG.get("services", "agent")
            worker_class_name = CONFIG.get("services", "worker")

            logger.debug("Importing agent service class %s", agent_class_name)
            logger.debug("Importing worker service class %s", worker_class_name)

            worker_class = None

            try:
                agent_class = import_class(agent_class_name)
                if worker_class_name:
                    logger.info("Importing class %s", worker_class_name)
                    worker_class = import_class(worker_class_name)
                    logger.info("Imported class: %s", worker_class)

            except Exception as ex:
                logging.error(ex)
                return

            logging.info("Starting agent_class %s", agent_class)
            logging.info("Starting worker_class %s", worker_class)

            agent = agent_class(
                context.obj["database"],
                context.obj["dburi"],
                pool=pool,
                config=config,
                port=port,
                workerport=workerport,
                backend=backend,
                name=name,
                user=user,
                clean=clean,
                size=size,
                cpus=cpus,
                workerclass=worker_class,
                broker=broker,
            )
        else:
            agent = AgentService(
                context.obj["database"],
                context.obj["dburi"],
                pool=pool,
                config=config,
                port=port,
                workerport=workerport,
                backend=backend,
                name=name,
                user=user,
                clean=clean,
                size=size,
                cpus=cpus,
                broker=broker,
            )

        agent.start()


@cli.group()
@click.pass_context
def web(context):
    """
    Web server admin
    """
    pass


@web.command(name="start")
@click.option("-p", "--port", default=8001, help="Listen port")
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
        logger.info("Shutting down...")
