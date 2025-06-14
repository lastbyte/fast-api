from sqlmodel import Session,select
from app.connectors.db.postgres import SessionDep
from app.models.db.schema import UserRole
from datetime import datetime
from app.models.requests.schema import CreateUserRoleRequest


async def create_user_role(db: SessionDep, user_role_request: CreateUserRoleRequest):
    try:
        user_role = UserRole(role_name=user_role_request.role_name, created_at=datetime.now(), updated_at=datetime.now())
        db.add(user_role)
        db.commit()
        db.refresh(user_role)
        return user_role
    except Exception as e:
        raise Exception(f"Error creating user role: {e}")
    

async def get_user_role(db: Session, user_role_id: int):
    try:
        user_roles = db.exec(select(UserRole).where(UserRole.id == user_role_id)).all()
        return user_roles[0]
    except Exception as e:
        raise Exception(f"Error getting user role: {e}")
    return None
    

async def update_user_role(db: Session, user_role_id: int, user_role_request: CreateUserRoleRequest):
    try:
        user_role = await get_user_role(db=db, user_role_id=user_role_id)

        if user_role:
            user_role.role_name = user_role_request.role_name
            user_role.updated_at = datetime.now()
            db.commit()
            db.refresh(user_role)
            return user_role
        else:
            raise Exception(f"User role with id {user_role_id} not found")
    except Exception as e:
        raise Exception(f"Error updating user role: {e}")
    
    
async def delete_user_role(db: SessionDep, user_role_id: int):
    try:
        user_role = await get_user_role(db=db, user_role_id=user_role_id)
        db.delete(user_role)
        db.commit()
    except Exception as e:
        raise Exception(f"Error deleting user role: {e}")
    

def get_all_user_roles(db: SessionDep):
    try:
        user_roles = db.exec(select(UserRole)).all()
        return user_roles
    except Exception as e:
        raise Exception(f"Error getting all user roles: {e}")