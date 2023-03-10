from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    PSQL_DSN: PostgresDsn
    STATE_TYPE: str
    ELASTIC_HOST: str
    ELASTIC_LOGIN: str
    ELASTIC_PASSWORD: str
    SCHEMA_SRC: str = '../utils/es_schema.json'
    INDEX_NAME: str = 'movies'
    DATA_CHUNK: int = 20
    STATE_FILE_PATH: str
    SLEEP_DURATION: int = 5
    REDIS_HOST: str

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
