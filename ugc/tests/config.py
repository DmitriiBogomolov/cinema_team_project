from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class TestConfig(Base):
    test_token: str
    base_url: str = 'http://localhost:8000'


class MongoConfig(Base):
    uri: str

    class Config:
        env_prefix = 'mongo_'


test_config = TestConfig()
mongo_config = MongoConfig()
