from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class Settings(BaseSettings):
    PSQL_DSN: PostgresDsn
    USE_STATE: bool
    ELASTIC_HOST: str
    ELASTIC_LOGIN: str
    ELASTIC_PASSWORD: str
    ELASTIC_SRT_PATH: str
    SCHEMA_SRC: str = '../utils/es_schema.json'
    INDEX_NAME: str = 'movies'
    DATA_CHUNK: int = 20
    STATE_FILE_PATH: str
    SLEEP_DURATION: int = 5

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
