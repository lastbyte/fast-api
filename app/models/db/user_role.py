from app.models.db.base import BaseModel
from sqlmodel import Field, Relationship
from typing import List, Optional

class UserRole(BaseModel, table=True):
    __tablename__ = "user_roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(nullable=False)
    users: List["User"] = Relationship(back_populates="role", sa_relationship_kwargs={"lazy": "selectin"})