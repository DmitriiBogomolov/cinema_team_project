import pytest
from elasticsearch import Elasticsearch
from redis import Redis

from tests.functional.settings import config
from tests.functional.testdata import es_mapping
from tests.functional.testdata.mocks import mock_genres


@pytest.fixture(scope='session')
def es_client() -> Elasticsearch:
    es_client = Elasticsearch(
        hosts=f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}',
        validate_cert=False,
        use_ssl=False
    )
    yield es_client
    es_client.close()


@pytest.fixture(scope='session')
def redis() -> Redis:
    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB
    )
    return redis


@pytest.fixture(scope='session', autouse=True)
def create_schemas(es_client: Elasticsearch) -> None:
    es_mapping.create_schemas(es_client)


@pytest.fixture(scope='function', autouse=True)
def clear_redis(redis: Redis) -> None:
    redis.flushall()


@pytest.fixture(scope='function')
def load_genres(es_client) -> None:
    es_client.delete_by_query(index='genres', body={'query': {'match_all': {}}})

    for genre in mock_genres.models:
        es_client.index(
            index='genres',
            id=genre.id,
            body=genre.dict()
        )

    es_client.indices.refresh(index='genres')

    return
