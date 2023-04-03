from logging import config as logging_config

from pydantic import BaseSettings

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AppConfig(BaseSettings):
    project_name: str = 'movies'
    redis_host: str = 'redis'
    redis_port: int = 6379
    redis_db: int = 2

    elastic_host: str = 'es01'
    elastic_port: int = 9200

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PITConfig(BaseSettings):
    pit_max_age: int = 20  # in seconds
    use_pit_rotation: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class CacheConfig(BaseSettings):
    use_caching: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = AppConfig()
pit_config = PITConfig()
cache_config = CacheConfig()
