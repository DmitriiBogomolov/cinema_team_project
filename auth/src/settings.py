from pydantic import BaseSettings


class AppSettings(BaseSettings):
    PG_PASSWORD: str = '123qwe'
    PG_USER: str = 'app'
    PG_DB: str = 'auth_database'
    PG_HOST: str = 'localhost'
    PG_PORT: str = 5437
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRES: int = 15 * (60)  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES: int = 30 * (24 * 60 * 60)  # 30 days
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6388

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
