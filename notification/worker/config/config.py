from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '../.env.example'
        env_file_encoding = 'utf-8'


class MongoConfig(Base):
    uri: str

    class Config:
        env_prefix = 'mongo_'


class RabbitConfig(Base):
    uri: str

    class Config:
        env_prefix = 'rabbit_'


class WorkerEmailConfig(Base):
    login: str
    password: str
    domain: str
    smtp_host: str
    smtp_port: int

    def get_email_from(self):
        return f'{self.login}@{self.domain}'

    class Config:
        env_prefix = 'email_'


rabbit_config = RabbitConfig()
worker_email_config = WorkerEmailConfig()
mongo_config = MongoConfig()
