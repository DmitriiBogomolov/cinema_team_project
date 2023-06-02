from dataclasses import dataclass

import pytest
import psycopg2
from psycopg2.extensions import connection, cursor
from redis import Redis

from config import config


@dataclass
class PSQL:
    conn: connection
    cursor: cursor


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


def clear_db(db: PSQL) -> None:
    db.cursor.execute(open('tests/functional/sql/truncate.sql', 'r').read())
    db.conn.commit()


def clear_redis(redis: Redis) -> None:
    redis.flushall()
