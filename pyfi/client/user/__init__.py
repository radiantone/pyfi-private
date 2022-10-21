import logging
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyfi.config import CONFIG
from pyfi.db.model import UserModel

db = CONFIG.get("database", "uri")

engine = create_engine(db)
setattr(engine, "uri", db)
session = sessionmaker(bind=engine)()
setattr(engine, "session", session)

try:
    if CONFIG.has_section("login"):
        user = CONFIG.get("login", "user")
        password = CONFIG.get("login", "password")
        try:
            USER: Optional[UserModel] = (
                session.query(UserModel).filter_by(name=user, password=password).first()
            )

            logging.debug(f"{USER} logged in.")
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
