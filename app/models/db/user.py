import time
from app.models.db.base import BaseModel
from sqlmodel import Field, Relationship
from typing import List, Optional

from app.common.constants import UserStatus


class UserRole(BaseModel, table=True):
    __tablename__ = "user_roles"

    role_name: str = Field(nullable=False)

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

    class Config:
        from_attributes = True
    

