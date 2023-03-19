import json
from typing import AsyncIterator

import httpx
import pytest
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from main import app
from mocks import mock_genres, mock_persons


@pytest.fixture(scope='module')
def anyio_backend() -> str:
    return 'asyncio'


@pytest.fixture(scope='module')
async def client() -> AsyncIterator[httpx.AsyncClient]:
    es = AsyncElasticsearch(hosts=['localhost:9201'])
    redis = Redis(host='127.0.0.1', port='6380')

    def override_elastic():
        return es

    def override_redis():
        return redis

    await prepare_elastic(es)

    app.dependency_overrides[get_elastic] = override_elastic
    app.dependency_overrides[get_redis] = override_redis

    async with httpx.AsyncClient(app=app, base_url='http://testserver') as client:
        yield client

    await es.close()
    await redis.close()


async def prepare_elastic(es_client):

    await create_schema(es_client, 'persons', 'tests/es_schemas/persons_schema.json')
    await create_schema(es_client, 'genres', 'tests/es_schemas/genres_schema.json')

    await load_person_fixtures(es_client)
    await load_genres_fixtures(es_client)


async def create_schema(es_client: AsyncElasticsearch, index_name: str, schema_src: str) -> None:

    await es_client.indices.delete(index=index_name, ignore=[400, 404])

    with open(schema_src) as schema_file:
        index_schema = json.load(schema_file)
        await es_client.indices.create(index=index_name, body=index_schema)


async def load_person_fixtures(es_client: AsyncElasticsearch) -> None:
    for person in mock_persons.list_:
        await es_client.index(
            index='persons',
            id=person.id,
            document=person.dict()
        )


async def load_genres_fixtures(es_client: AsyncElasticsearch) -> None:
    for genre in mock_genres.list_:
        await es_client.index(
            index='genres',
            id=genre.id,
            document=genre.dict()
        )
