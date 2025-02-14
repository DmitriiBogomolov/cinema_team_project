import pytest
import psycopg2
from redis import Redis

from app.core.config import config
from tests.functional.models import PSQL
from tests.conftest import clear_db, clear_redis


@pytest.fixture(scope='session')
def db() -> PSQL:
    conn = psycopg2.connect(
        dbname=config.postgres_db,
        user=config.postgres_user,
        password=config.postgres_password,
        host=config.postgres_host,
        port=config.postgres_port
    )
    cursor = conn.cursor()
    yield PSQL(
        conn=conn,
        cursor=cursor
    )
    cursor.close()
    conn.close()


@pytest.fixture(scope='session')
def redis() -> Redis:
    redis = Redis(
        host=config.redis_host,
        port=config.redis_port
    )
    return redis


@pytest.fixture(autouse=True)
def clean_up(db: PSQL, redis: Redis) -> None:
    clear_db(db)
    clear_redis(redis)


@pytest.fixture()
def pg_data(db: PSQL, clean_up) -> None:
    db.cursor.execute(open('tests/functional/sql/load_data.sql', 'r').read())
    db.conn.commit()
