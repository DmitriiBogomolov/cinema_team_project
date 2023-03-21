from logging import config as logging_config
from pydantic import BaseSettings
from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppConfig(BaseSettings):
    PROJECT_NAME: str = 'movies'
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    REDIS_DB: int = 2

    ELASTIC_HOST: str = 'es01'
    ELASTIC_PORT: int = 9200

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PITConfig(BaseSettings):
    PIT_MAX_AGE: int = 20  # in seconds
    USE_PIT_ROTATION: bool = True


config = AppConfig()
pit_config = PITConfig()
