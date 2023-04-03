from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppConfig(BaseSettings):
    project_name: str = 'movies'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 2

    elastic_host: str = 'localhost'
    elastic_port: int = 9200

    API_HOST: str = 'localhost'
    API_PORT: int = 8000

    @property
    def API_URL(self):
        return f'http://{self.API_HOST}:{self.API_PORT}'

    @property
    def ELASTIC_URL(self):
        return f'{self.elastic_host}:{self.elastic_port}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = AppConfig()
