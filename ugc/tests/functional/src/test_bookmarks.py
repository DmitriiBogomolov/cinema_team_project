from http import HTTPStatus

import requests

from tests.config import test_config
from tests.functional.fixtures.mongo import mongo_fixture
from tests.utils import compare


BASE_URL = test_config.base_url
URL = f'{BASE_URL}/api/v1/bookmarks'
TOKEN = test_config.test_token


def test_get_bookmarks(mongo_fixtures):
    response = requests.get(URL)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        URL, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert (
        sorted(response.json(), key=lambda x: x['movie_id'])
        ==
        sorted(mongo_fixture['bookmarks'], key=lambda x: x['movie_id'])
    )


def test_post_bookmark():
    response = requests.get(
        URL, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []

    response = requests.post(
        URL, json=mongo_fixture['bookmarks'][0]
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.post(
        URL, json=mongo_fixture['bookmarks'][0],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.post(
        URL, json=mongo_fixture['bookmarks'][1],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.get(
        URL, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert compare(response.json(), mongo_fixture['bookmarks'])
