from pydantic import BaseSettings


class AppSettings(BaseSettings):
    PG_PASSWORD: str = '123qwe'
    PG_USER: str = 'app'
    PG_DB: str = 'auth_database'
    PG_HOST: str = 'localhost'
    PG_PORT: str = 5437

    @property
    def POSTGRES_DSN(self):
        return f'postgresql://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


app_settings = AppSettings()
