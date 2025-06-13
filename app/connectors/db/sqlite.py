# Code above omitted 👆
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session,create_engine

from app.common.logger import Logger


logger = Logger(__name__)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    logger.info("creating database")
    SQLModel.metadata.create_all(engine)