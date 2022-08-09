from .model.models import ActionModel as Action
from .model.models import AgentModel as Agent
from .model.models import Base
from .model.models import FlowModel as Flow
from .model.models import LogModel as Log
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
from .model.models import WorkerModel as Worker
from .postgres import _compile_drop_table
from sqlalchemy import create_engine, event
import configparser

CONFIG = configparser.ConfigParser()

from pathlib import Path

HOME = str(Path.home())

ini = HOME + "/pyfi.ini"

CONFIG.read(ini)


@event.listens_for(Processor, 'after_update')
def receive_after_update(mapper, connection, target):
    import json
    import logging
    import redis
    from sqlalchemy import inspect

    redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

    state = inspect(target)
    # Publish to redis, pubsub, which gets sent to browser
    has_changes = False
    logging.info("RECEIVE_AFTER_COMMIT Processor %s", str(target.name))
    for attr in state.attrs:
        hist = state.get_history(attr.key, True)

        if not hist.has_changes():
            continue

        has_changes = True

    if has_changes:
        logging.info("RECEIVE_AFTER_COMMIT CHANGED!")
        redisclient.publish(
            "global",
            json.dumps({"type": "processor", "name": target.name, "processor": json.loads(str(target))}),
        )
    else:
        logging.info("No changes!")


def get_session():
    from sqlalchemy.orm import sessionmaker, scoped_session

    _engine = create_engine(CONFIG.get("database", "uri"), isolation_level='READ UNCOMMITTED')
    _session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=_engine))

    return _session


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
