from datetime import datetime
from sqlmodel import Session
from app.models.db.user import User
from app.models.db.user_role import UserRole
from app.common.logger import Logger

logger = Logger(__name__)

def seed_user_roles(session: Session):
    """Seed initial user roles into the database"""
    try:
        # Check if roles already exist
        existing_roles = session.query(UserRole).all()
        if existing_roles:
            logger.info("User roles already exist, skipping seeding")
            return

        # Define initial roles
        roles = [
            UserRole(
                role_name="admin",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            UserRole(
                role_name="user",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            UserRole(
                role_name="guest",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]

        # Add roles to session
        for role in roles:
            session.add(role)
        
        # Commit the changes
        session.commit()
        logger.info("Successfully seeded user roles")
    except Exception as e:
        logger.error(f"Error seeding user roles: {e}")
        session.rollback()
        raise e 
    

def seed_users(session: Session):
    """Seed initial users into the database"""
    try:
        # Check if users already exist
        existing_users = session.query(User).all()
        if existing_users:
            logger.info("Users already exist, skipping seeding")
            return
        
        # Define initial users
        users = [
            User(
                username="admin",
                email="admin@example.com",
                password="5f4dcc3b5aa765d61d8327deb882cf99",
                role_id=1,
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            User(
                username="user",
                email="user@example.com",
                password="5f4dcc3b5aa765d61d8327deb882cf99",
                role_id=2,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Add users to session
        for user in users:
            session.add(user)
            
        # Commit the changes
        session.commit()
        logger.info("Successfully seeded users")
    except Exception as e:
        logger.error(f"Error seeding users: {e}")
        session.rollback()
        raise e 