from pydantic import BaseSettings


class Config(BaseSettings):
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_host: str = 'db'
    postgres_port: str = 5432
    redis_host: str = 'redis'
    redis_port: int = 6379
    swagger_url: str = '/swagger'
    refresh_token_exp: int = 60 * 60 * 24 * 15  # 15 days
    debug: bool = False
    rate_limit_tokens: int = 20  # value of tokens in a bucket
    rate_limit_token_increment: int = 20  # number of accumulated tokens every second
    jaeger_host: str = 'jaeger'
    jaeger_port: int = '6831'

    @property
    def sqlalchemy_database_uri(self) -> str:
        return 'postgresql://{}:{}@{}:{}/{}'.format(self.postgres_user,
                                                    self.postgres_password,
                                                    self.postgres_host,
                                                    self.postgres_port,
                                                    self.postgres_db)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
