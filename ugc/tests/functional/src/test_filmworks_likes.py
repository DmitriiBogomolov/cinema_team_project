from http import HTTPStatus

import requests

from tests.config import test_config
from tests.functional.fixtures.mongo import mongo_fixture
from tests.utils import compare


BASE_URL = test_config.test_url
URL = f'{BASE_URL}/api/v1/movies'
TOKEN = test_config.test_token


def test_get_filmwork_likes(filmworks_likes_fix):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    get_url = f'{URL}/{movie_id}/likes'

    response = requests.get(get_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [mongo_fixture['filmworks_likes'][0]]


def test_post_filmwork_likes():
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    url = f'{URL}/{movie_id}/likes'

    response = requests.get(
        url, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []

    response = requests.post(
        url, json=mongo_fixture['filmworks_likes'][0]
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.post(
        url, json=mongo_fixture['filmworks_likes'][0],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.get(
        url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert compare(
        response.json(),
        [mongo_fixture['filmworks_likes'][0]]
    )


def test_delete_filmwork_like(filmworks_likes_fix):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]

    url = f'{URL}/{movie_id}/like'

    response = requests.delete(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.delete(
        url, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_get_filmwork_likes_count(filmworks_likes_fix):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    url = f'{URL}/{movie_id}/likes/count'

    response = requests.get(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'count': 1}


def test_get_filmwork_likes_average(filmworks_likes_fix):
    movie_id = mongo_fixture["filmworks_likes"][0]["entity_id"]
    url = f'{URL}/{movie_id}/likes/average'

    response = requests.get(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"average": 10.0}
