from datetime import datetime
from sqlmodel import Session
from app.models.db.schema import Permission, User, UserRole, UserRolePermissionLink
from app.common.logger import Logger

logger = Logger(__name__)

def seed_permissions(session: Session):
    """Seed initial permissions into the database"""
    try:
        # Check if permissions already exist
        existing_permissions = session.query(Permission).all()
        if existing_permissions:
            logger.info("Permissions already exist, skipping seeding")
            return
        
        # Define initial permissions
        permissions = [
            Permission(
                permission_name="create_user",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="read_user",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="update_user",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="delete_user",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="create_user_role",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="read_user_role",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="update_user_role",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="delete_user_role",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="create_permission",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            ),
            Permission(
                permission_name="read_permission",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="update_permission",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Permission(
                permission_name="delete_permission",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Add permissions to session
        for permission in permissions:
            session.add(permission)
        
        # Commit the changes
        session.commit()
        logger.info("Successfully seeded permissions")
    except Exception as e:
        logger.error(f"Error seeding permissions: {e}")
        session.rollback()
        raise e 
    
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
    

def seed_user_role_permissions(session: Session):
    """Seed initial user role permissions into the database"""
    try:
        # Check if user role permissions already exist
        existing_user_role_permissions = session.query(UserRolePermissionLink).all()
        if existing_user_role_permissions:
            logger.info("User role permissions already exist, skipping seeding")
            return

        # Define initial user role permissions
        user_role_permissions = [
            UserRolePermissionLink(
                role_id=1,
                permission_id=1
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=2
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=3
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=4
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=5
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=6
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=7
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=8
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=9
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=10
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=11
            ),
            UserRolePermissionLink(
                role_id=1,
                permission_id=12
            ),
        ]
        
        # Add user role permissions to session
        for user_role_permission in user_role_permissions:
            session.add(user_role_permission)
        
        # Commit the changes
        session.commit()
        logger.info("Successfully seeded user role permissions")
    except Exception as e:
        logger.error(f"Error seeding user role permissions: {e}")
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