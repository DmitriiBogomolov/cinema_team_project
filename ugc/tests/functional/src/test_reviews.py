from http import HTTPStatus

import requests

from tests.config import test_config
from tests.functional.fixtures.mongo import mongo_fixture
from tests.utils import compare


BASE_URL = test_config.base_url
URL = f'{BASE_URL}/api/v1/reviews'
TOKEN = test_config.test_token


def test_get_review(mongo_fixtures):
    cur_url = f'{URL}?movie_id={mongo_fixture["reviews"][0]["movie_id"]}'
    response = requests.get(cur_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        cur_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [mongo_fixture['reviews'][0]]


def test_post_review():
    get_url = f'{URL}?movie_id={mongo_fixture["reviews"][0]["movie_id"]}'
    post_url = URL

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    response = requests.post(
        post_url, json=mongo_fixture['reviews'][0]
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.post(
        post_url, json=mongo_fixture['reviews'][0],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.post(
        post_url, json=mongo_fixture['reviews'][1],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert compare(
        response.json()[0],
        mongo_fixture['reviews'][0]
    )


def test_get_review_likes(mongo_fixtures):
    get_url = f'{URL}/{mongo_fixture["reviews_likes"][0]["entity_id"]}/likes'

    response = requests.get(get_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [mongo_fixture['reviews_likes'][0]]


def test_post_review_likes():
    get_url = f'{URL}/{mongo_fixture["reviews_likes"][0]["entity_id"]}/likes'
    post_url = f'{URL}/likes'

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []

    response = requests.post(
        post_url, json=mongo_fixture['reviews_likes'][0]
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.post(
        post_url, json=mongo_fixture['reviews_likes'][0],
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.CREATED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert compare(
        response.json(),
        [mongo_fixture['reviews_likes'][0]]
    )


def test_delete_review_like(mongo_fixtures):
    delete_url = f'{URL}/likes/{mongo_fixture["reviews_likes"][0]["_id"]}'
    get_url = f'{URL}/{mongo_fixture["reviews_likes"][0]["entity_id"]}/likes'

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
