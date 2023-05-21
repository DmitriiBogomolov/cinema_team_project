from pydantic import BaseSettings


class AppSettings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = 'db'
    POSTGRES_PORT: str = 5432
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379
    SWAGGER_URL: str = '/swagger'

    @property
    def POSTGRES_DSN(self) -> str:
        return 'postgresql://{}:{}@{}:{}/{}'.format(self.POSTGRES_USER,
                                                    self.POSTGRES_PASSWORD,
                                                    self.POSTGRES_HOST,
                                                    self.POSTGRES_PORT,
                                                    self.POSTGRES_DB)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
