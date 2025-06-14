# Code above omitted 👆
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session,create_engine
from app.common.configuration import config

from app.common.logger import Logger


logger = Logger(__name__)
DATABASE_URL = "postgresql+psycopg2://postgres:yourpassword@localhost:5432/mydatabase"
pg_url = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_POST}/{config.DB_NAME}"

engine = create_engine(pg_url)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    logger.info("creating database")
    SQLModel.metadata.create_all(engine)