from pydantic_settings import BaseSettings

class Configuration(BaseSettings):

    APP_PORT : int = None
    APP_ENV : str = 'dev'
    JWT_TOKEN_SECRET : str = None

    class Config:
        env_file = ".env"
        env_file_encoding="utf-8"


config = Configuration()


