
from typing import List
from pydantic import BaseModel, Field

from app.models.db.schema import Permission, User, UserProfile


class SelfUserProfileResponse(BaseModel):
    user : User
    profile : UserProfile | None = None

class UserProfileResponse(BaseModel):
    profile : UserProfile | None = None


class UserPermissionListResponse(BaseModel):
    permissions : List[Permission] = Field(default=[])
    total_count : int = Field(default=0)
    page_size : int = Field(default=10)
    page_num : int = Field(default=1)


class UserPermissionCreateResponse(BaseModel):
    permission : Permission

class UserPermissionUpdateResponse(BaseModel):
    permission : Permission

class UserPermissionDeleteResponse(BaseModel):
    success : bool = Field(default=True)