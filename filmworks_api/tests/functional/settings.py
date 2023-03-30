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

    API_HOST: str = 'api'
    API_PORT: int = 8000

    @property
    def API_URL(self):
        return f'http://{self.API_HOST}:{self.API_PORT}'

    @property
    def ELASTIC_URL(self):
        return f'{self.ELASTIC_HOST}:{self.ELASTIC_PORT}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = AppConfig()
