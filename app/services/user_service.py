from typing import List
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy import func
from app.common.logger import Logger
from app.exceptions.database_exceptions import EntityExists
from app.models.requests.create_user_request import CreateUserRequest, LoginRequest
from app.models.user import User

logger = Logger(__name__)

class ListFilters : 
    sort_dir : str = 'asc'
    sort_column : str = 'id'
    q : str = ""


async def get_user(db: Session, user_id : int) -> User :
    try:
        users = db.exec(select(User).where(User.id == user_id)).all()
        return users[0]
    except Exception:
        logger.error("Error occurred while fetching user from database")
    return None


async def get_user_by_email(db: Session, email: str): 
    try:
        users = db.get(select(User).where(User.email == email)).all()
        return users[0]
    except Exception:
        logger.error("Error occurred while fetching user from db")
    return None


async def login_user(db: Session, login_request : LoginRequest):
    try:
        users = db.exec(select(User).where(User.email == login_request.email and User.password == login_request.password)).all()
        return users[0]
    except Exception:
        logger.error("Error occurred while fetching user from db")
    return None

async def create_user(db: Session, create_user_request: CreateUserRequest) -> User:
    try:
        existing_user = await get_user_by_email(db, create_user_request.email)

        if existing_user :
            raise EntityExists();

        user = User(first_name=create_user_request.first_name, last_name=create_user_request.last_name,
                    email=create_user_request.email, password=create_user_request.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as ex:
        logger.error("Exception occurred while creating user")
        raise ex


async def list_users(db: Session, q: str, sort_dir : str, sort_column : str, page_num: int, page_size: int):
    try:
        offset = (page_num-1) * page_size
        limit = page_size


        user_count_result = db.exec(select(func.count()).select_from(User))
        user_count = user_count_result.one()

        users_result = db.exec(select(User).offset(offset).limit(limit))
        users = [user.model_dump() for user in  users_result.all()]

        return user_count, users
    except Exception as ex:
        logger.error("Exception occurred while fetching user list from database")
        logger.error(ex)
