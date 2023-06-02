import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from redis import Redis

from app import create_app
from tests.functional.models import PSQL


pytest_plugins = [
    'tests.functional.conf_fixtures.db_conftest',
    'tests.functional.conf_fixtures.utils_conftest',
]


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


def clear_db(db: PSQL) -> None:
    db.cursor.execute(open('tests/functional/sql/truncate.sql', 'r').read())
    db.conn.commit()


def clear_redis(redis: Redis) -> None:
    redis.flushall()
