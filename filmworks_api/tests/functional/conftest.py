import asyncio
import uuid
from typing import AsyncIterator, Optional
from dataclasses import dataclass

import aiohttp
from multidict import CIMultiDictProxy
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from src.models.genre import Genre as GenreModel
from src.models.film import Filmwork as FilmModel
from tests.functional.settings import config
from tests.functional.testdata.mocks.mock_genres import GENRES_LIST
from tests.functional.testdata.mocks.mock_films import FILMS_LIST
from tests.functional.testdata.mocks.mock_persons import TEST_PERSONS


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest_asyncio.fixture(scope='function')
async def make_get_request(session):
    async def inner(
        method: str, params: Optional[dict] = None
    ) -> HTTPResponse:
        params = params or {}
        url = config.API_URL + '/api/v1' + method
        response = await session.get(url, params=params)
        return HTTPResponse(
            body=await response.json(),
            headers=response.headers,
            status=response.status,
        )

    return inner


@pytest_asyncio.fixture(scope='session')
async def session() -> AsyncIterator[aiohttp.ClientSession]:
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture(scope='session')
async def es() -> AsyncIterator[AsyncElasticsearch]:
    es = AsyncElasticsearch(
        hosts=config.ELASTIC_URL,
        validate_cert=False,
        use_ssl=False
    )
    yield es
    await es.close()


@pytest_asyncio.fixture(scope='session')
async def redis() -> Redis:
    redis = Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db
    )
    return redis


@pytest_asyncio.fixture(scope='function', autouse=True)
async def clear_redis(redis: Redis) -> None:
    await redis.flushall()


@pytest_asyncio.fixture(scope='function')
async def clear_genres(es: AsyncElasticsearch) -> None:
    await es.delete_by_query(index='genres', body={'query': {'match_all': {}}})
    await es.indices.refresh(index='genres')


@pytest_asyncio.fixture(scope='function')
async def load_genres(es: AsyncElasticsearch, clear_genres: None) -> None:
    for genre in GENRES_LIST:
        await es.index(
            index='genres',
            id=genre['id'],
            document=genre
        )

    await es.indices.refresh(index='genres')

    return [GenreModel(**item) for item in GENRES_LIST]


@pytest_asyncio.fixture(scope='session')
async def random_uuid():
    return uuid.uuid4()


@pytest_asyncio.fixture(scope='function')
async def clear_films(es: AsyncElasticsearch) -> None:
    await es.delete_by_query(index='movies', body={'query': {'match_all': {}}})
    await es.indices.refresh(index='movies')


@pytest_asyncio.fixture(scope='function')
async def load_films(es: AsyncElasticsearch, clear_films: None) -> None:
    for film in FILMS_LIST:
        await es.index(
            index='movies',
            id=film['id'],
            document=film
        )

    await es.indices.refresh(index='movies')

    return [FilmModel(**item) for item in FILMS_LIST]


@pytest_asyncio.fixture(scope='function')
async def clear_persons(es: AsyncElasticsearch) -> None:
    await es.delete_by_query(index='persons', body={'query': {'match_all': {}}})
    await es.indices.refresh(index='persons')


@pytest_asyncio.fixture(scope='function')
async def load_persons(es: AsyncElasticsearch, clear_persons: None) -> None:
    for person in TEST_PERSONS:
        await es.index(
            index='persons',
            id=person['id'],
            document=person
        )

    await es.indices.refresh(index='persons')

    # return [FilmModel(**item) for item in FILMS_LIST]
