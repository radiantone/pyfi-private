from .model.models import ActionModel as Action
from .model.models import AgentModel as Agent
from .model.models import Base
from .model.models import FlowModel as Flow
from .model.models import LogModel as Log
from .model.models import NodeModel as Node
from .model.models import PlugModel as Plug
from .model.models import BaseModel, AgentModel, NodeModel, WorkerModel, DeploymentModel
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


@event.listens_for(BaseModel, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    import json
    import logging
    import redis
    from sqlalchemy.orm import object_session

    redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

    if not isinstance(target, (Processor, DeploymentModel, WorkerModel, NodeModel, AgentModel)):
        logging.info("receive_after_update: Skipping for %s", target.__class__.__name__)
        return

    has_changes = object_session(target).is_modified(target, include_collections=False)
    logging.info("receive_after_update: %s",target)

    if has_changes or isinstance(target, Processor):
        logging.info("RECEIVE_AFTER_COMMIT CHANGED! Class %s",target.__class__.__name__)
        redisclient.publish(
            "global",
            json.dumps({"type": target.__class__.__name__, "name": target.name, "processor": json.loads(str(target))})
        )
    else:
        logging.debug("No changes!")


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
