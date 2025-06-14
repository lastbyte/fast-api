from datetime import datetime, timedelta
from typing import List
from sqlmodel import Session, select
from sqlalchemy import func
from app.common.logger import Logger
from app.common.utils import generate_random_string
from app.connectors.cache.redis import get_redis_connector
from app.exceptions.database_exceptions import DbException
from app.models.requests.schema import CreateUserRequest, LoginRequest, UpdatePasswordRequest
from app.models.db.schema import User, UserSignUpVerification
from app.common.constants import UserSignUpVerificationStatus, UserStatus
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


async def update_password(db: Session, user_id: int, update_password_request: UpdatePasswordRequest) -> User:
    try:
        user = await get_user(db=db, user_id=user_id)
        if not user:
            raise Exception(f"User with id {user_id} not found")
        
        if update_password_request.existing_password != user.password:
            raise Exception("Existing passwords does not match")
        
        user.password = update_password_request.new_password
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        raise DbException("Exception occurred while updating password")


async def create_user(db: Session, create_user_request: CreateUserRequest) -> User:
    """
    Create a new user from the request data
    
    Args:
        db (Session): Database session
        create_user_request (CreateUserRequest): User creation request data
        
    Returns:
        User: Created user object
        
    Raises:
        DbException: If user with same email already exists
        ValueError: If role_id is invalid
    """
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, create_user_request.email)
        if existing_user:
            raise DbException(f"User with email {create_user_request.email} already exists")

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

        user_sign_up_verification = UserSignUpVerification(
            user_id=user.id,
            verification_code=generate_random_string(length=32),
            expires_at=datetime.now() + timedelta(minutes=10)
        )

        db.add(user_sign_up_verification)
        db.commit()
        db.refresh(user_sign_up_verification)
        
        logger.info(f"Successfully created user with email: {user.email}")
        return user
        
    except DbException as e:
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
        raise DbException("Exception occurred while fetching user list from database")


async def logout(token : str):
    try:
        redis_connector = get_redis_connector()
        await redis_connector.write(token, True, ttl=60 * 60 * 24 * 14)
        return True
    except Exception as ex:
        logger.error(f"error occurred while logging out user : {str(ex)}")
        raise DbException(f"error occurred while logging out user : {str(ex)}")
    

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
        raise DbException("Exception occurred while updating user role")
    

async def verify_user_sign_up(db: Session, user_id: int, verification_code: str) -> User:
    try:
        user_sign_up_verification = db.exec(select(UserSignUpVerification).where(UserSignUpVerification.user_id == user_id and UserSignUpVerification.verification_code == verification_code)).one()
        user = db.exec(select(User).where(User.id == user_id)).one()

        if not user:
            raise Exception(f"User with id {user_id} not found")
        
        if user.status == UserStatus.VERIFIED:
            raise Exception(f"User with id {user_id} already verified")
        
        if not user_sign_up_verification:
            raise Exception(f"User with id {user_id} not found")
        
        if user_sign_up_verification.status == UserSignUpVerificationStatus.VERIFIED:
            raise Exception(f"User with id {user_id} already verified")
        
        if user_sign_up_verification.status == UserSignUpVerificationStatus.EXPIRED:
            raise Exception(f"User with id {user_id} verification code expired")
        
        if user_sign_up_verification.expires_at < datetime.now():
            user_sign_up_verification.status = UserSignUpVerificationStatus.EXPIRED
            db.commit()
            db.refresh(user_sign_up_verification)
            raise Exception(f"User with id {user_id} verification code expired")
        
        user_sign_up_verification.status = UserSignUpVerificationStatus.VERIFIED
        db.commit()
        db.refresh(user_sign_up_verification)
        return user
    except Exception:
        raise DbException("Exception occurred while verifying user sign up")