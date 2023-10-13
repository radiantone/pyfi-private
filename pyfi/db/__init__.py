# type: ignore

import configparser
import logging
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine, event

from .model.models import ActionModel as Action
from .model.models import AgentModel
from .model.models import AgentModel as Agent
from .model.models import Base, BaseModel, DeploymentModel
from .model.models import FlowModel as Flow
from .model.models import LogModel as Log
from .model.models import NodeModel
from .model.models import NodeModel as Node
from .model.models import PlugModel as Plug
from .model.models import ProcessorModel as Processor
from .model.models import QueueModel as Queue
from .model.models import RoleModel as Role
from .model.models import SchedulerModel as Scheduler
from .model.models import SettingsModel as Settings
from .model.models import SocketModel as Socket
from .model.models import TaskModel as Task
from .model.models import UserModel as User
from .model.models import WorkerModel
from .model.models import WorkerModel as Worker
from .postgres import _compile_drop_table

CONFIG = configparser.ConfigParser()


HOME = str(Path.home())

ini = HOME + "/pyfi.ini"


CONFIG.read(ini)


@event.listens_for(BaseModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    import json
    import logging

    import redis
    from sqlalchemy.orm import object_session

    redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

    if not isinstance(
        target, (Processor, DeploymentModel, WorkerModel, NodeModel, AgentModel)
    ):
        logging.debug(
            "receive_after_update: Skipping for %s", target.__class__.__name__
        )
        return

    has_changes = object_session(target).is_modified(target, include_collections=False)
    logging.debug("receive_after_update: %s", target)

    if has_changes or isinstance(target, Processor):
        logging.debug(
            "RECEIVE_AFTER_COMMIT CHANGED! Class %s", target.__class__.__name__
        )
        redisclient.publish(
            "global",
            json.dumps(
                {
                    "type": target.__class__.__name__,
                    "name": target.name,
                    "object": json.loads(str(target)),
                }
            ),
        )
    else:
        logging.debug("No changes!")


@contextmanager
def get_session(**kwargs):
    # from pymongo import MongoClient
    logging.debug("get_session: Creating session")

    from sqlalchemy.orm import scoped_session, sessionmaker
    from sqlalchemy.pool import NullPool

    user = kwargs["user"] if "user" in kwargs else None
    uri = CONFIG.get("database", "uri")

    # client = MongoClient(CONFIG.get("mongodb", "uri"))
    if user is not None:
        # pyfidb = client["pyfi"]
        # users = pyfidb["users"]
        user_id = user["sub"]
        email = user["email"]

        password = user_id.split("|")[1]
        uname = email.split("@")[0] + "." + password
        # user = users.find_one({ "_id": uname})
        # print(user)
        # Get user from database, get login password
        # login = {}
        uri = (
            CONFIG.get("database", "base")
            .replace("USER", uname)
            .replace("PASSWORD", password)
        )
        logging.info("DB URI FOR USER: %s", uri)

    _engine = create_engine(uri, isolation_level="AUTOCOMMIT", poolclass=NullPool)
    conn = _engine.connect()
    session = scoped_session(sessionmaker(bind=_engine))

    try:
        logging.debug("get_session: Yielding session")
        yield session
    except:
        import traceback

        print(traceback.format_exc())
        logging.debug("get_session: Rollback session")
        session.rollback()
    else:
        logging.debug("get_session: Commit session")
        session.commit()
    finally:
        logging.debug("get_session: Closing session")
        # session.expunge_all()
        session.close()
        logging.debug("get_session: Closing connection")
        conn.close()


__all__ = (
    "get_session",
    "Worker",
    "Agent",
    "Role",
    "Processor",
    "User",
    "Queue",
    "Log",
    "Plug",
    "Socket",
    "Flow",
    "Action",
    "Settings",
    "Node",
    "Task",
    "Scheduler",
    "Base",
)
