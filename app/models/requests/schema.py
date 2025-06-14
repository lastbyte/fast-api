from pydantic import BaseModel,Field

class CreateUserRequest(BaseModel): 
    email : str = Field(description="email of the user", examples=["user@test.com"])
    password : str = Field(description="Encrypted password of the user", examples=["5f4dcc3b5aa765d61d8327deb882cf99"])
    first_name : str | None = Field(description="first name of the user", examples=["John"])
    last_name : str | None = Field(description="last name of the user", examples=["Doe"])
    role_id : int = Field(description="role id of the user", examples=[1])

class CreateUserProfileRequest(BaseModel):
    profile_picture: str | None = Field(default=None, description="Profile picture of the user")
    bio: str | None = Field(default=None, description="Bio of the user")
    location: str | None = Field(default=None, description="Location of the user")
    website: str | None = Field(default=None, description="Website of the user")
    contact_number: str | None = Field(default=None, description="Contact number of the user")


class UpdateUserProfileRequest(BaseModel):
    profile_picture: str | None = Field(default=None, description="Profile picture of the user")
    bio: str | None = Field(default=None, description="Bio of the user")
    location: str | None = Field(default=None, description="Location of the user")
    website: str | None = Field(default=None, description="Website of the user")
    contact_number: str | None = Field(default=None, description="Contact number of the user")


class UpdatePasswordRequest(BaseModel):
    existing_password: str = Field(description="Existing password of the user", examples=["5f4dcc3b5aa765d61d8327deb882cf99"])
    new_password: str = Field(description="Encrypted password of the user", examples=["5f4dcc3b5aa765d61d8327deb882cf99"])


class LoginRequest(BaseModel): 
    email : str = Field(description="email of the user", examples=["user@test.com"])
    password : str = Field(description="Encrypted password of the user", examples=["5f4dcc3b5aa765d61d8327deb882cf99"])


class CreateUserRoleRequest(BaseModel):
    role_name: str = Field(description="name of the role", examples=["admin", "user", "moderator"])

class UpdateUserRoleRequest(BaseModel):
    role_name: str = Field(description="name of the role", examples=["admin", "user", "moderator"])


class UserPermissionUpdateRequest(BaseModel):
    permission_name: str = Field(description="name of the permission", examples=["create_user", "update_user", "delete_user"])


class UserPermissionCreateRequest(BaseModel):
    permission_name: str = Field(description="name of the permission", examples=["create_user", "update_user", "delete_user"])