from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env.example'
        env_file_encoding = 'utf-8'


class AppConfig(Base):
    project_name: str = 'notification_service'
    debug: bool = True

    authjwt_secret_key: str
    auth_url: str
    auth_token: str


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
        template = 'postgresql+asyncpg://{}:{}@{}:{}/{}'
        return template.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db
        )

    class Config:
        env_prefix = 'postgres_'


class RabbitConfig(Base):
    uri: str

    class Config:
        env_prefix = 'rabbit_'


config = AppConfig()
postgres_config = PostgresConfig()
rabbit_config = RabbitConfig()
