from collections import namedtuple

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


Schema = namedtuple('Schema', 'index_name, schema_src')


class Settings(BaseSettings):
    PSQL_DSN: PostgresDsn

    ELASTIC_HOST: str
    ELASTIC_LOGIN: str
    ELASTIC_PASSWORD: str

    REDIS_HOST: str

    STATE_TYPE: str
    STATE_FILE_PATH: str

    SLEEP_DURATION: int = 5
    DATA_CHUNK: int = 20

    SCHEMAS_DESTINATION = [
        Schema('movies', '../utils/filmworks_schema.json'),
        Schema('genres', '../utils/genres_schema.json'),
        Schema('persons', '../utils/persons_schema.json')
    ]

    class Config:
        case_sensitive = True
        env_file = '.env'


settings = Settings()
