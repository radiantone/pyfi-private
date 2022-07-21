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


def get_session():
    import configparser
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import event

    CONFIG = configparser.ConfigParser()

    from pathlib import Path
    HOME = str(Path.home())

    ini = HOME + "/pyfi.ini"

    CONFIG.read(ini)

    _engine = create_engine(CONFIG.get("database", "uri"))
    _session = sessionmaker(bind=_engine)()

    @event.listens_for(_session, 'before_commit')
    def receive_after_commit(session):
        import redis
        import json

        redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

        for obj in session:
            if isinstance(obj, Processor):
                # Publish to redis, pubsub, which gets sent to browser
                redisclient.publish(
                    "global",
                    json.dumps({'type':'processor','processor':str(obj)}),
                )

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
