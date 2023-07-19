from http import HTTPStatus

import requests

from tests.config import test_config
from tests.functional.fixtures.mongo import mongo_fixture
from tests.utils import compare


BASE_URL = test_config.base_url
URL = f'{BASE_URL}/api/v1/movies_likes'
TOKEN = test_config.test_token


def test_get_filmwork_likes(mongo_fixtures):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    get_url = f'{URL}?movie_id={movie_id}'

    response = requests.get(get_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [mongo_fixture['filmworks_likes'][0]]


def test_post_filmwork_likes():
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    get_url = f'{URL}?movie_id={movie_id}'
    post_url = URL

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []

    response = requests.post(
        post_url, json=mongo_fixture['filmworks_likes'][0]
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.post(
        post_url, json=mongo_fixture['filmworks_likes'][0],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert compare(
        response.json(),
        [mongo_fixture['filmworks_likes'][0]]
    )


def test_delete_filmwork_like(mongo_fixtures):
    like_id = mongo_fixture["filmworks_likes"][0]["_id"]
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]

    delete_url = f'{URL}/{like_id}'
    get_url = f'{URL}?movie_id={movie_id}'

    response = requests.delete(delete_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.delete(
        delete_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_filmwork_likes_count(mongo_fixtures):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    get_url = f'{URL}/count?movie_id={movie_id}'

    response = requests.get(get_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'count': 1}


def test_get_filmwork_likes_average(mongo_fixtures):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    get_url = f'{URL}/average?movie_id={movie_id}'

    response = requests.get(get_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"average": 10.0}
