from datetime import datetime
from typing import List
from sqlmodel import Session, select
from sqlalchemy import func
from app.common.logger import Logger
from app.connectors.cache.redis import get_redis_connector
from app.exceptions.database_exceptions import EntityExists
from app.models.requests.schema import CreateUserRequest, LoginRequest
from app.models.db.schema import User
from app.common.constants import UserStatus
from app.services import user_role_service

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
        raise Exception("Error occurred while fetching user from database")
    return None


async def get_user_by_email(db: Session, email: str): 
    try:
        users = db.exec(select(User).where(User.email == email)).all()
        return users[0]
    except Exception:
        raise Exception("Error occurred while fetching user from db")
    return None


async def login_user(db: Session, login_request : LoginRequest):
    try:
        users = db.exec(select(User).where(User.email == login_request.email and User.password == login_request.password)).all()
        return users[0]
    except Exception:
        raise Exception("Error occurred while fetching user from db")
    return None

async def create_user(db: Session, create_user_request: CreateUserRequest) -> User:
    """
    Create a new user from the request data
    
    Args:
        db (Session): Database session
        create_user_request (CreateUserRequest): User creation request data
        
    Returns:
        User: Created user object
        
    Raises:
        EntityExists: If user with same email already exists
        ValueError: If role_id is invalid
    """
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, create_user_request.email)
        if existing_user:
            raise EntityExists(f"User with email {create_user_request.email} already exists")

        # Create user object from request data
        user_data = create_user_request.model_dump()
        user = User(
            **user_data,
            status=UserStatus.CREATED,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            create_by=0  # TODO: Replace with actual user ID when implementing authentication
        )
        
        # Save to database
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Successfully created user with email: {user.email}")
        return user
        
    except EntityExists as e:
        logger.error(str(e))
        raise e
    except Exception as ex:
        logger.error(f"Error creating user: {str(ex)}")
        db.rollback()
        raise ex


async def list_users(db: Session, q: str, sort_dir : str , sort_column : str , page_num: int = 1, page_size: int = 10):
    try:
        offset = (page_num-1) * page_size
        limit = page_size

        user_count_result = db.exec(select(func.count()).select_from(User))
        user_count = user_count_result.one()

        users_result = db.exec(select(User).offset(offset).limit(limit).order_by(sort_column)).all()
        users = [user.model_dump() for user in users_result]

        return user_count, users
    except Exception:
        raise Exception("Exception occurred while fetching user list from database")


async def logout(token : str):
    try:
        redis_connector = get_redis_connector()
        await redis_connector.write(token, True, ttl=60 * 60 * 24 * 14)
        return True
    except Exception as ex:
        logger.error(f"error occurred while logging out user : {str(ex)}")
        return False
    

async def update_user_role(db: Session, user_id: int, role_id: int):
    try:
        user = await get_user(db=db, user_id=user_id)
        if not user:
            raise Exception(f"User with id {user_id} not found")

        user_role = await user_role_service.get_user_role(db=db, user_role_id=role_id)
        if not user_role:
            raise Exception(f"Role with id {role_id} not found")
        
        user.role_id = role_id
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        raise Exception("Exception occurred while updating user role")