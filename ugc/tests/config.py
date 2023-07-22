from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class TestConfig(Base):
    test_token: str
    test_url: str


class MongoConfig(Base):
    uri: str

    class Config:
        env_prefix = 'mongo_'


test_config = TestConfig()
mongo_config = MongoConfig()
