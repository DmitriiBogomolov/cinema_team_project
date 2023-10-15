from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class TestConfig(Base):
    test_token: str
    api_url: str = 'http://notification:8000/api/v1/events'


class PostgresConfig(Base):
    password: str
    user: str
    db: str
    host: str
    port: str
    future: bool
    echo: bool

    @property
    def sqlalchemy_uri(self) -> str:
        template = 'postgresql+psycopg2://{}:{}@{}:{}/{}'
        return template.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db
        )

    class Config:
        env_prefix = 'postgres_'


test_config = TestConfig()
postgres_config = PostgresConfig()
