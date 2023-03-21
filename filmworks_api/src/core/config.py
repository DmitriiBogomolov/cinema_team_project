from logging import config as logging_config
from pydantic import BaseSettings, Field
from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppConfig(BaseSettings):
    PROJECT_NAME: str = Field(..., env='PROJECT_NAME')
    REDIS_HOST: str = Field(..., env='REDIS_HOST')
    REDIS_PORT: int = Field(..., env='REDIS_PORT')
    REDIS_DB: int = Field(..., env='REDIS_DB')

    ELASTIC_HOST: str = Field(..., env='ELASTIC_HOST')
    ELASTIC_PORT: int = Field(..., env='ELASTIC_PORT')

    PIT_MAX_AGE: int = 20  # in seconds
    USE_PIT_ROTATION: bool = True


config = AppConfig()
