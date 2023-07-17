from http import HTTPStatus

import requests

from tests.config import test_config
from tests.functional.fixtures.mongo import mongo_fixture


BASE_URL = test_config.base_url
URL = f'{BASE_URL}/api/v1/reviews'
TOKEN = test_config.test_token


def test_get_review(mongo_fixtures):
    response = requests.get(
        f'{URL}?movie_id={mongo_fixture["reviews"][0]["movie_id"]}'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        f'{URL}?movie_id={mongo_fixture["reviews"][0]["movie_id"]}',
        headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK

    assert 1 == 1
