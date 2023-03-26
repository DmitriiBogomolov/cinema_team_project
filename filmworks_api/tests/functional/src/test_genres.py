import requests
import orjson
from http import HTTPStatus

from elasticsearch import Elasticsearch

from tests.functional.settings import config
from tests.functional.testdata.mocks import mock_genres


def test_genre_by_id(es_client: Elasticsearch, load_genres: list[dict]):
    resp = requests.get(f'{config.API_URL}/api/v1/genres/{mock_genres.models[0].id}')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == orjson.loads(mock_genres.response_models[0].json(by_alias=True))


def test_genres_list(es_client: Elasticsearch, load_genres: list[dict]):
    resp = requests.get(f'{config.API_URL}/api/v1/genres/')

    assert resp.status_code == HTTPStatus.OK
    assert len(resp.json()) == 3
    assert resp.json() == [orjson.loads(mock.json(by_alias=True))
                           for mock in mock_genres.response_models]


def test_not_found(es_client: Elasticsearch, load_genres: list[dict]):
    resp = requests.get(f'{config.API_URL}/api/v1/genres/05fb2223-dabf-40e9-9924-20446fadf325')

    assert resp.status_code == HTTPStatus.NOT_FOUND
