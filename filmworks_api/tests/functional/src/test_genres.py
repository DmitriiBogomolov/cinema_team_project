from datetime import datetime, timedelta
from http import HTTPStatus

import aiohttp
import pytest

from src.models.genre import Genre as GenreModel

from ..settings import config
from ..testdata.mocks.mock_genres import ResponseGenreModel

URL = config.API_URL


@pytest.mark.asyncio
async def test_genre_not_found(
        session: aiohttp.ClientSession,
        clear_genres: None
):

    url = f'{URL}/api/v1/genres/05fb2223-dabf-40e9-9924-20446fadf39'
    async with session.get(url) as resp:
        json = await resp.json()
        assert resp.status == HTTPStatus.NOT_FOUND
        assert json.get('detail') == 'No genre with that UUID found.'


@pytest.mark.asyncio
async def test_genre_by_id(
        session: aiohttp.ClientSession,
        load_genres: list[GenreModel]
):

    genre = load_genres[0]
    url = f'{URL}/api/v1/genres/{genre.id}'
    async with session.get(url) as resp:
        json = await resp.json()
        assert resp.status == HTTPStatus.OK
        assert json == ResponseGenreModel(**genre.dict()).get_json()


@pytest.mark.asyncio
async def test_genres_list(
        session: aiohttp.ClientSession,
        load_genres: list[GenreModel]
):

    sorted_genres = sorted(load_genres, key=lambda x: x.name)
    url = f'{URL}/api/v1/genres/'
    async with session.get(url) as resp:
        json = await resp.json()
        assert resp.status == HTTPStatus.OK
        assert len(json) == len(sorted_genres)
        assert json == [ResponseGenreModel(**genre.dict()).get_json()
                        for genre in sorted_genres]


@pytest.mark.asyncio
async def test_genres_field_types(
        session: aiohttp.ClientSession,
        load_genres: list[GenreModel]
):

    url = f'{URL}/api/v1/genres/'
    async with session.get(url) as resp:
        json = await resp.json()
        for obj in json:
            assert isinstance(obj.get('uuid'), str)
            assert isinstance(obj.get('name'), str)


@pytest.mark.asyncio
async def test_genres_execution_time(
        session: aiohttp.ClientSession,
        load_genres: list[GenreModel]
):

    start_time = datetime.now()
    url = f'{URL}/api/v1/genres/'
    async with session.get(url) as resp:
        await resp.json()
        exec_time = datetime.now() - start_time
        assert resp.status == HTTPStatus.OK
        assert exec_time <= timedelta(milliseconds=200)
