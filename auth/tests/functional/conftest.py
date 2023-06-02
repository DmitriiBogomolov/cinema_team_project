from dataclasses import dataclass

import pytest
from psycopg2.extensions import connection, cursor
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from redis import Redis
from flask_jwt_extended import create_access_token

from app import create_app
from db_conftest import *


@dataclass
class PSQL:
    conn: connection
    cursor: cursor


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


@pytest.fixture(scope='function')
def jwt_headers(app: Flask) -> FlaskClient:
    with app.app_context():
        access_token = create_access_token({'id': '11111169-6712-4666-8116-7c4eaf111111'})
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        return headers


@pytest.fixture()
def runner(app: Flask) -> FlaskCliRunner:
    return app.test_cli_runner()
