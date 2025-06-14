import time
from app.models.db.base import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional

from app.common.constants import UserStatus
from app.models.db.user_role import UserRole


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
    role: Optional[UserRole] = Relationship(back_populates="users", sa_relationship_kwargs={"lazy": "selectin"})

    @classmethod
    def get_user_by_email(cls, email: str):
        return cls.query.filter(cls.email == email).first()
    
    @classmethod
    def get_user_by_id(cls, id: int):
        return cls.query.filter(cls.id == id).first()
    
    @classmethod
    def get_users_by_role(cls, role: str):
        return cls.query.filter(cls.role.role_name == role).all()

