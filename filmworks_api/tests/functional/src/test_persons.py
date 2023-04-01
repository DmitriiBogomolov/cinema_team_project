from http import HTTPStatus

import aiohttp
import pytest

from tests.functional.settings import config
from tests.functional.testdata.mocks.mock_persons import TEST_PERSON

URL = config.API_URL + '/api/v1/persons'


@pytest.mark.asyncio
async def test_get_person_by_non_existant_uuid_returns_404(
        session: aiohttp.ClientSession,
        random_uuid
):
    url = f'{URL}{random_uuid}'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_person_by_correct_uuid_returns_OK(
        session: aiohttp.ClientSession,
):
    url = f"""{URL}/{TEST_PERSON['id']}"""
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_person_by_correct_uuid_returns_correct_data(
        session: aiohttp.ClientSession,
):
    url = f"""{URL}/{TEST_PERSON['id']}"""
    async with session.get(url) as resp:
        api_response = await resp.json()
        assert api_response == TEST_PERSON['response_ref']


@pytest.mark.asyncio
async def test_get_person_films(
        session: aiohttp.ClientSession,
):
    url = f"""{URL}/{TEST_PERSON['id']}/film"""
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        person_films = await resp.json()
        assert len(person_films) == 3
        assert person_films == TEST_PERSON['films_ref']


@pytest.mark.asyncio
async def test_person_search(
        session: aiohttp.ClientSession,
):
    url = f"""{URL}/search?query=Aaron"""
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        person_films = await resp.json()
        assert len(person_films) == 6


@pytest.mark.asyncio
async def test_person_search_pagination(
        session: aiohttp.ClientSession,
):
    url = f"""{URL}/search?query=Aaron&page_size=5"""
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        person_films = await resp.json()
        assert len(person_films) == 5


@pytest.mark.asyncio
async def test_person_search_pagination_offset(
        session: aiohttp.ClientSession,
):
    url = f"""{URL}/search?query=Aaron&page_number=2&page_size=5"""
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        person_films = await resp.json()
        assert len(person_films) == 1
