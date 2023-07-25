from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class AppConfig(Base):
    project_name: str = 'movies'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 2

    elastic_host: str = 'http://localhost'
    elastic_port: int = 9200

    authjwt_secret_key: str

    dsn: str


class PITConfig(Base):
    pit_max_age: int = 20  # in seconds
    use_pit_rotation: bool = False


class CacheConfig(Base):
    use_caching: bool = False


class LoggerConfig(Base):
    host: str = 'localhost'
    port: int = 5044

    class Config:
        env_prefix = 'logstash_'


config = AppConfig()
pit_config = PITConfig()
cache_config = CacheConfig()
logger_config = LoggerConfig()
