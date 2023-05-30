from dataclasses import dataclass

import pytest
import psycopg2
from psycopg2.extensions import connection, cursor
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from redis import Redis

from app import create_app
from config import config


@dataclass
class PSQL:
    conn: connection
    cursor: cursor


@pytest.fixture(scope='session')
def db() -> PSQL:
    conn = psycopg2.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
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
        host=config.REDIS_HOST,
        port=config.REDIS_PORT
    )
    return redis


@pytest.fixture()
def app(db: PSQL, redis: Redis) -> Flask:
    app = create_app()
    app.config.update({
        'TESTING': True,
    })
    yield app
    clear_db(db)
    clear_redis(redis)


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()


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
