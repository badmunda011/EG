import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# the secret configuration specific things
from ..Config import config
from ..core.logger import logging
from Eaglebot.core import session

LOGS = logging.getLogger(__name__)


def start() -> scoped_session:
    database_url = (
        config.DB_URI.replace("postgres:", "postgresql:")
        if "postgres://" in config.DB_URI
        else config.DB_URI
    )
    engine = create_engine(database_url)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    LOGS.error(
        "DB_URI is not configured. Features depending on the database might have issues."
    )
    LOGS.error(str(e))
