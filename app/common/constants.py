
from enum import Enum


APP_NAME = "FastAPI Boilerplate"
APP_DESCRIPTION = "FastAPI Boilerplate"

API_PREFIX = "/api"


class UserStatus(int,Enum):
    INACTIVE=0
    CREATED = 1
    VERIFIED = 2
