import time
from app.models.db.base import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

from app.common.constants import UserStatus


class UserRolePermissionLink(SQLModel, table=True):
    __tablename__ = "user_role_permissions"

    role_id: Optional[int] = Field(
        default=None,
        foreign_key="user_roles.id",
        primary_key=True
    )
    permission_id: Optional[int] = Field(
        default=None,
        foreign_key="permissions.id",
        primary_key=True
    )


class UserRole(BaseModel, table=True):
    __tablename__ = "user_roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(nullable=False, unique=True)
    users: List["User"] = Relationship(back_populates="role")
    permissions: List["Permission"] = Relationship(
        back_populates="roles",
        link_model=UserRolePermissionLink
    )

    class Config:
        from_attributes = True


class User(BaseModel, table=True):
    __table_args__ = {"extend_existing": True}
    __tablename__="users"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str | None = Field(default=None, description="First Name of the user",nullable=True)
    last_name: str | None = Field(default=None, description="Last Name of the user",nullable=True,)
    email: str | None = Field(default=None, description="Email of the user",nullable=False, unique=True)
    password : str | None = Field(default=None, nullable=False, exclude=True)
    status: UserStatus | None = Field(default=UserStatus.CREATED, nullable=False)
    role_id: Optional[int] = Field(default=None, foreign_key="user_roles.id", nullable=False)
    role: Optional["UserRole"] = Relationship(back_populates="users")

    class Config:
        from_attributes = True


class Permission(BaseModel, table=True):
    __tablename__ = "permissions"

    permission_name: str = Field(nullable=False, unique=True)
    roles: List["UserRole"] = Relationship(
        back_populates="permissions",
        link_model=UserRolePermissionLink
    )
    
    class Config:
        from_attributes = True



    

