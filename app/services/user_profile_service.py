from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from app.exceptions.database_exceptions import DbException
from app.models.db.schema import UserProfile
from app.models.requests.schema import CreateUserProfileRequest, UpdateUserProfileRequest


async def get_user_profile(db: Session, user_id: int) -> UserProfile:
    try:
        user_profile = db.exec(select(UserProfile).where(UserProfile.user_id == user_id)).one()
        return user_profile
    except NoResultFound:
        return None
    except Exception as e:
        raise DbException(f"Error getting user profile: {e}")
    

async def create_user_profile(db: Session, user_id: int, user_profile_request: CreateUserProfileRequest) -> UserProfile:
    try:
        existing_user_profile = db.exec(select(UserProfile).where(UserProfile.user_id == user_id)).one()
        if existing_user_profile:
            raise DbException("User profile already exists")
        user_profile = UserProfile(user_id=user_id, **user_profile_request.model_dump())
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
        return user_profile
    except Exception as e:
        raise DbException(f"Error creating user profile: {e}")

async def update_user_profile(db: Session, user_id: int, user_profile_request: UpdateUserProfileRequest) -> UserProfile:
    try:
        user_profile = db.exec(select(UserProfile).where(UserProfile.user_id == user_id)).one()
        if not user_profile:
            raise DbException("User profile not found")
        user_profile.update(user_profile_request.model_dump())
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
        return user_profile
    except Exception as e:
        raise DbException(f"Error updating user profile: {e}")
    

async def delete_user_profile(db: Session, user_id: int) -> UserProfile:
    try:
        user_profile = db.exec(select(UserProfile).where(UserProfile.user_id == user_id)).one()
        if not user_profile:
            raise DbException("User profile not found")
        db.delete(user_profile)
        db.commit()
        return user_profile
    except Exception as e:
        raise DbException(f"Error deleting user profile: {e}")