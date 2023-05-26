import configparser
import pathlib

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configure.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo = True)
DBSession = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    The get_db function is a context manager that returns a database session.
    It also ensures that the session is closed when the request ends.

    :return: A generator
    """
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
