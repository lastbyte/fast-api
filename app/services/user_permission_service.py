from fastapi import HTTPException
from sqlalchemy import func
from sqlmodel import Session, select
from app.exceptions.database_exceptions import DbException
from app.models.db.schema import Permission, UserRolePermissionLink


async def get_permission_by_id(db: Session, permission_id: int):
    try:
        permission = db.exec(select(Permission).where(Permission.id == permission_id)).first()
        return permission
    except Exception as e:
        raise DbException(f"Error getting permission by id: {e}")
    

async def create_permission(db: Session, permission: Permission):
    try:
        existing_permission = db.exec(select(Permission).where(Permission.permission_name == permission.permission_name)).first()
        if existing_permission:
            raise HTTPException(status_code=400, detail=f"Permission with name {permission.permission_name} already exists")
        
        db.add(permission)
        db.commit()
        db.refresh(permission)
        return permission
    except Exception as e:
        raise DbException(f"Error creating permission: {e}")
    

async def update_permission(db: Session, permission_id: int, permission: Permission):
    try:
        existing_permission = db.exec(select(Permission).where(Permission.id == permission_id)).first()
        if not existing_permission:
            raise HTTPException(status_code=404, detail=f"Permission with id {permission_id} does not exist")
        
        existing_permission.permission_name = permission.permission_name
        db.commit()
        db.refresh(existing_permission)
        return existing_permission
    except Exception as e:
        raise DbException(f"Error updating permission: {e}")
    

async def delete_permission(db: Session, permission_id: int):
    try:
        permission = db.exec(select(Permission).where(Permission.id == permission_id)).first()
        if not permission:
            raise HTTPException(status_code=404, detail=f"Permission with id {permission_id} does not exist")
        
        db.delete(permission)
        db.commit()
        return True
    except Exception as e:
        raise DbException(f"Error deleting permission: {e}")


async def get_all_permissions(db: Session, page_num: int, page_size: int):
    try:
        permissions = db.exec(select(Permission).offset((page_num - 1) * page_size).limit(page_size)).all()
        permission_count_result = db.exec(select(func.count()).select_from(Permission))
        permission_count = permission_count_result.one()
        return permissions, permission_count
    except Exception as e:
        raise DbException(f"Error getting all permissions: {e}")
    

async def get_permission_by_user_role(db: Session, user_role_id: int):
    try:
        permissions = db.exec(select(Permission).join(UserRolePermissionLink).where(UserRolePermissionLink.role_id == user_role_id)).all()
        return permissions
    except Exception as e:
        raise DbException(f"Error getting permission by user role: {e}")