# Dummy token validator
from functools import wraps
import time
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.common.configuration import config
from app.connectors.cache.redis import get_redis_connector
from app.models.db.schema import User

token_auth_scheme = HTTPBearer()
token_algoritm = 'HS256'


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token = credentials.credentials
    return token

def get_token(credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    token = credentials.credentials
    return token


def create_auth_token(user: User):
    return encrypt_token({"user": user.model_dump(),
                  "expires_at": time.time() + (14 * 24 * 60 * 60)})

def verify_jwt_token(token : str) : 
    decoded = decode_jwt_token(token=token)
    current_time = time.time()

    if current_time < decoded["expires_at"]:
        return decoded
    return None


def encrypt_token(token_data: any):
    return jwt.encode(token_data, config.JWT_TOKEN_SECRET, algorithm=token_algoritm)


def decode_jwt_token(token: str):
    return jwt.decode(token, config.JWT_TOKEN_SECRET, algorithms=[token_algoritm])


def authenticate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Find the request object in args or kwargs
        request: Request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        if not request:
            request = kwargs.get("request")
        if not request:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request object not found")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

        token = auth_header.split(" ")[1]
        try:
            payload = decode_jwt_token(token)
            # Optionally, you can attach payload to request.state for downstream use
            expires_at = payload["expires_at"]
            if expires_at < time.time():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
            
            redis_connector = get_redis_connector()
            expired_token = await redis_connector.read(token)

            if expired_token is not None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
            
            request.state.user = payload["user"]
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        return await func(*args, **kwargs)
    return wrapper


def validate_permissions(allowed_permissions: list[int]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find the request object in args or kwargs
            request: Request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                request = kwargs.get("request")
            if not request:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Request object not found")

            if request.state.user["role_id"] not in allowed_permissions:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to access this resource")


            return await func(*args, **kwargs)
        return wrapper
    return decorator
