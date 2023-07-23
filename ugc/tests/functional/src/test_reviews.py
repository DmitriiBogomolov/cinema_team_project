from http import HTTPStatus

import requests

from tests.config import test_config
from tests.functional.fixtures.mongo import mongo_fixture
from tests.utils import compare


BASE_URL = test_config.test_url
URL = f'{BASE_URL}/api/v1/reviews'
TOKEN = test_config.test_token


def test_get_review(reviews_fix):
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


def test_get_review_likes(reviews_fix, reviews_likes_fix):
    get_url = f'{URL}/{mongo_fixture["reviews_likes"][0]["entity_id"]}/likes'

    response = requests.get(get_url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.get(
        get_url, headers={'Authorization': f'Bearer {TOKEN}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [mongo_fixture['reviews_likes'][0]]


def test_post_review_likes(reviews_fix):
    get_url = f'{URL}/{mongo_fixture["reviews_likes"][0]["entity_id"]}/likes'
    post_url = f'{URL}/{mongo_fixture["reviews"][0]["_id"]}/like'

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


def test_delete_review_likes(reviews_fix, reviews_likes_fix):
    url = f'{URL}/{mongo_fixture["reviews"][0]["_id"]}/like'
    response = requests.delete(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response = requests.delete(
        url,
        headers={'Authorization': f'Bearer {TOKEN}'}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
