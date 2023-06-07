import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='function')
def jwt_headers(app: Flask) -> FlaskClient:
    with app.app_context():
        access_token = create_access_token({
            'id': '11111169-6712-4666-8116-7c4eaf111111',
            'top_secret': True

        })
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        return headers
