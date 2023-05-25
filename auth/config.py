from pydantic import BaseSettings


class Config(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'db'
    POSTGRES_PORT: str = 5432
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    SWAGGER_URL: str = '/swagger'
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 15  # 15 days

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return 'postgresql://{}:{}@{}:{}/{}'.format(self.POSTGRES_USER,
                                                    self.POSTGRES_PASSWORD,
                                                    self.POSTGRES_HOST,
                                                    self.POSTGRES_PORT,
                                                    self.POSTGRES_DB)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Config()
