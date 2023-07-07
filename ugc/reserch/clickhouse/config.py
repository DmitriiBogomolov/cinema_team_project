from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class ClickhouseSettings(Base):
    host: str = 'localhost'
    port: int = 9000
    user: str = 'admin'
    password: str = 123

    class Config:
        env_prefix = 'clickhouse_'


clickhouse_settings = ClickhouseSettings()
