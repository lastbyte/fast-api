from datetime import datetime
import time
from app.models.db.base import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

from app.common.constants import UserSignUpVerificationStatus, UserStatus

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
    profile: Optional["UserProfile"] = Relationship(back_populates="user")

    class Config:
        from_attributes = True

    
class UserSignUpVerification(BaseModel, table=True):
    __tablename__ = "user_sign_up_verifications"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", nullable=False)
    verification_code: str = Field(nullable=False)
    status: UserSignUpVerificationStatus = Field(default=UserSignUpVerificationStatus.PENDING, nullable=False)
    expires_at: datetime = Field(nullable=False)

    class Config:
        from_attributes = True
    


class UserProfile(BaseModel, table=True):
    __tablename__ = "user_profiles"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", nullable=False)
    user: Optional["User"] = Relationship(back_populates="profile")
    profile_picture: str | None = Field(default=None, description="Profile picture of the user",nullable=True)
    bio: str | None = Field(default=None, description="Bio of the user",nullable=True)
    location: str | None = Field(default=None, description="Location of the user",nullable=True)
    website: str | None = Field(default=None, description="Website of the user",nullable=True)
    contact_number: str | None = Field(default=None, description="Contact number of the user",nullable=True)
    address: str | None = Field(default=None, description="Address of the user",nullable=True)
    city: str | None = Field(default=None, description="City of the user",nullable=True)
    state: str | None = Field(default=None, description="State of the user",nullable=True)
    country: str | None = Field(default=None, description="Country of the user",nullable=True)
    zip_code: str | None = Field(default=None, description="Zip code of the user",nullable=True)
    date_of_birth: datetime | None = Field(default=None, description="Date of birth of the user",nullable=True)
    gender: str | None = Field(default=None, description="Gender of the user",nullable=True)
    marital_status: str | None = Field(default=None, description="Marital status of the user",nullable=True)
    occupation: str | None = Field(default=None, description="Occupation of the user",nullable=True)
    education: str | None = Field(default=None, description="Education of the user",nullable=True)
    religion: str | None = Field(default=None, description="Religion of the user",nullable=True)
    caste: str | None = Field(default=None, description="Caste of the user",nullable=True)
    nationality: str | None = Field(default=None, description="Nationality of the user",nullable=True)


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
        link_model=UserRolePermissionLink,
        sa_relationship="many-to-many"
    )

    class Config:
        from_attributes = True


class Permission(BaseModel, table=True):
    __tablename__ = "permissions"

    permission_name: str = Field(nullable=False, unique=True)
    roles: List["UserRole"] = Relationship(back_populates="permissions", link_model=UserRolePermissionLink, sa_relationship="many-to-many")
    
    class Config:
        from_attributes = True



    

