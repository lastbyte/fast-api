
from pydantic import BaseModel


class InvalidUserRequest(BaseModel):
    errors : str | list[str]