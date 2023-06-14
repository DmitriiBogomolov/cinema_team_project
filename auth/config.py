from pydantic import BaseSettings


class Base(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class YandexOAuthConfig(Base):
    name: str = 'yandex'
    client_id: str
    client_secret: str
    authorize_url: str = 'https://oauth.yandex.ru/authorize'
    access_token_url: str = 'https://oauth.yandex.ru/token'

    class Config:
        env_prefix = 'yandex_'


class GoogleOAuthConfig(Base):
    name: str = 'google'
    client_id: str
    client_secret: str
    authorize_url: str = 'https://accounts.google.com/o/oauth2/auth'
    access_token_url: str = 'https://accounts.google.com/o/oauth2/token'
    client_kwargs: dict = {'scope': 'email'}
    server_metadata_url: str = 'https://accounts.google.com/.well-known/openid-configuration'

    class Config:
        env_prefix = 'google_'


class Config(Base):
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
    secret_key: str
    jwt_secret_key: str

    @property
    def sqlalchemy_database_uri(self) -> str:
        return 'postgresql://{}:{}@{}:{}/{}'.format(self.postgres_user,
                                                    self.postgres_password,
                                                    self.postgres_host,
                                                    self.postgres_port,
                                                    self.postgres_db)


yandex_config = YandexOAuthConfig()
google_config = GoogleOAuthConfig()
config = Config()
