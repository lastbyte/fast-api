from pydantic_settings import BaseSettings

class Configuration(BaseSettings):

    APP_PORT : int = None
    APP_ENV : str = 'dev'
    JWT_TOKEN_SECRET : str = None

    DB_USER :str = None
    DB_PASSWORD :str = None
    DB_HOST :str = None
    DB_POST: int = None
    DB_NAME : str = None

    REDIS_HOST : str  =None
    REDIS_PORT : str = None
    REDIS_KEY : str = None

    class Config:
        env_file = ".env"
        env_file_encoding="utf-8"


config = Configuration()


