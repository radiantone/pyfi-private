import logging

from sqlalchemy import MetaData, create_engine, literal_column
from sqlalchemy.orm import sessionmaker

from pyfi.config import CONFIG
from pyfi.db.model import (
    ActionModel,
    AgentModel,
    CallModel,
    FlowModel,
    LogModel,
    NodeModel,
    PlugModel,
    ProcessorModel,
    QueueModel,
    RoleModel,
    SchedulerModel,
    SettingsModel,
    SocketModel,
    TaskModel,
    UserModel,
    WorkerModel,
    oso,
)

db = CONFIG.get("database", "uri")
USER = None

engine = create_engine(db)
engine.uri = db
session = sessionmaker(bind=engine)()
engine.session = session

try:
    if CONFIG.has_section("login"):
        user = CONFIG.get("login", "user")
        password = CONFIG.get("login", "password")
        try:
            USER = (
                session.query(UserModel).filter_by(name=user, password=password).first()
            )
            logging.debug(f"{USER.name} logged in.")
        except Exception as ex:
            import traceback

            print(traceback.format_exc())
            print(f"Unable to log in {user}.")

except Exception as ex:
    print(
        "Database unavailable. Please check your configuration or ensure database server is running."
    )
finally:
    session.close()
