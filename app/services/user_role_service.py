from typing import List
from sqlmodel import Session,select
from app.connectors.db.postgres import SessionDep
from app.exceptions.database_exceptions import DbException
from app.models.db.schema import Permission, UserRole, UserRolePermissionLink
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
    

async def get_user_role_permissions(db: SessionDep, user_role_id: int):
    try:
        permissions = db.exec(select(Permission).join(UserRolePermissionLink).where(UserRolePermissionLink.role_id == user_role_id)).all()
        return permissions
    except Exception as e:
        raise Exception(f"Error getting user role permissions: {e}")
    

async def add_permission_to_user_role(db: SessionDep, user_role_id: int, permission_id: int):
    try:
        user_role_permission_link = UserRolePermissionLink(role_id=user_role_id, permission_id=permission_id)
        db.add(user_role_permission_link)
        db.commit()
    except Exception as e:
        raise DbException(f"Error adding permission to user role: {e}")
    

async def remove_permission_from_user_role(db: SessionDep, user_role_id: int, permission_id: int):
    try:
        user_role_permission_link = db.exec(select(UserRolePermissionLink).where(UserRolePermissionLink.role_id == user_role_id, UserRolePermissionLink.permission_id == permission_id)).first()
        db.delete(user_role_permission_link)
        db.commit()
    except Exception as e:
        raise DbException(f"Error removing permission from user role: {e}")
    

async def add_permissions_to_user_role(db: SessionDep, user_role_id: int, permission_ids: List[int]):
    try:
        for permission_id in permission_ids:
            user_role_permission_link = UserRolePermissionLink(role_id=user_role_id, permission_id=permission_id)
            db.add(user_role_permission_link)
        db.commit()
        return True
    except Exception as e:
        raise DbException(f"Error adding permissions to user role: {e}")
    

async def remove_permissions_from_user_role(db: SessionDep, user_role_id: int, permission_ids: List[int]):
    try:
        for permission_id in permission_ids:
            user_role_permission_link = db.exec(select(UserRolePermissionLink).where(UserRolePermissionLink.role_id == user_role_id, UserRolePermissionLink.permission_id == permission_id)).first()
            db.delete(user_role_permission_link)
        db.commit()
        return True
    except Exception as e:
        raise DbException(f"Error removing permissions from user role: {e}")