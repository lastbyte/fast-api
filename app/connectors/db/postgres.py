# Code above omitted 👆
from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session,create_engine
from app.common.configuration import config
from datetime import datetime

from app.common.logger import Logger
from app.models.db.user import User
from app.models.db.user_role import UserRole
from app.connectors.db.seeders import seed_user_roles, seed_users


logger = Logger(__name__)
pg_url = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_POST}/{config.DB_NAME}"

engine = create_engine(pg_url)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    logger.info("dropping database")
    SQLModel.metadata.drop_all(engine)

    logger.info("creating database")
    SQLModel.metadata.create_all(engine)
    
    # Seed initial data
    with Session(engine) as session:
        seed_user_roles(session)
        seed_users(session)
