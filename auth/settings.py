from pydantic import BaseSettings


class AppSettings(BaseSettings):
    PG_PASSWORD: str
    PG_USER: str
    PG_DB: str
    PG_HOST: str = 'db'
    PG_PORT: str = 5432
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 15 * (60)  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = 30 * (24 * 60 * 60)  # 30 days
    REDIS_HOST: str = 'redis'
    REDIS_PORT: int = 6379

    @property
    def POSTGRES_DSN(self) -> str:
        return 'postgresql://{}:{}@{}:{}/{}'.format(self.PG_USER,
                                                    self.PG_PASSWORD,
                                                    self.PG_HOST,
                                                    self.PG_PORT,
                                                    self.PG_DB)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
