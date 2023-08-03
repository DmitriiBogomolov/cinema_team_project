from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class AppConfig(Base):
    project_name: str = 'notification_service'
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    debug: bool = True

    authjwt_secret_key: str


class MongoConfig(Base):
    uri: str

    class Config:
        env_prefix = 'mongo_'


config = AppConfig()
mongo_config = MongoConfig()
