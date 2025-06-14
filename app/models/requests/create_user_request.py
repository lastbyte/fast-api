from pydantic import BaseModel,Field

class CreateUserRequest(BaseModel): 
    email : str = Field(description="email of the user", examples=["user@test.com"])
    password : str = Field(description="Encrypted password of the user", examples=["5f4dcc3b5aa765d61d8327deb882cf99"])
    first_name : str | None = Field(description="first name of the user", examples=["John"])
    last_name : str | None = Field(description="last name of the user", examples=["Doe"])


class LoginRequest(BaseModel): 
    email : str = Field(description="email of the user", examples=["user@test.com"])
    password : str = Field(description="Encrypted password of the user", examples=["5f4dcc3b5aa765d61d8327deb882cf99"])