import time
from app.models.db.base import BaseModel
from sqlmodel import Field

from app.common.constants import UserStatus


class User(BaseModel, table=True):
    
    __tablename__="users"

    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(default=None, description="First Name of the user",nullable=True)
    last_name: str | None = Field(default=None, description="Last Name of the user",nullable=True,)
    email: str | None = Field(default=None, description="Email of the user",nullable=False, unique=True)
    password : str | None = Field(default=None, nullable=False, exclude=True)
    status: UserStatus | None = Field(default=UserStatus.CREATED, nullable=False)

