from datetime import datetime, timedelta
from http import HTTPStatus

import aiohttp
import pytest

from src.models.film import Filmwork as FilmModel

from ..settings import config
from ..testdata.mocks.mock_films import ResponseFilmDetailModel, ResponseFilmModel, FILMS_LIST

URL = config.API_URL + '/api/v1/films'


@pytest.mark.asyncio
async def test_film_not_found(
        session: aiohttp.ClientSession,
        clear_films: None
):
    url = f'{URL}/3fa85f64-5717-4562-b3fc-2c963f66afa7'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.NOT_FOUND
        json = await resp.json()
        assert json.get('detail') == 'film not found'


@pytest.mark.asyncio
async def test_films_not_found(
        session: aiohttp.ClientSession,
        clear_films: None
):
    url = f'{URL}/'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert json == []


@pytest.mark.asyncio
async def test_film_by_id(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    film = load_films[0]
    url = f'{URL}/{film.id}'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert json == ResponseFilmDetailModel(**film.dict()).get_json()


@pytest.mark.asyncio
async def test_films_list(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    sorted_films = sorted(load_films, key=lambda x: x.imdb_rating, reverse=True)
    url = f'{URL}/?sort=-imdb_rating'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == len(FILMS_LIST)
        assert json == [ResponseFilmModel(**film.dict()).get_json()
                        for film in sorted_films]


@pytest.mark.asyncio
async def test_films_list_pagination(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    url = f'{URL}/?sort=-imdb_rating&page_size=3'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == 3


@pytest.mark.asyncio
async def test_films_list_pagination_offset(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    url = f'{URL}/?sort=-imdb_rating&page_size=4&page_number=3'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == 1


@pytest.mark.asyncio
async def test_films_by_genre(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    sorted_films = sorted(load_films[:5], key=lambda x: x.imdb_rating, reverse=True)
    url = f'{URL}/?genre=120a21cf-9097-479e-904a-13dd7198c1dd&sort=-imdb_rating'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == 5
        assert json == [ResponseFilmModel(**film.dict()).get_json()
                        for film in sorted_films]


@pytest.mark.asyncio
async def test_films_search(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    url = f'{URL}/search?query=Cooper'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == 3


@pytest.mark.asyncio
async def test_films_search_pagination(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    url = f'{URL}/search?query=Cooper&page_size=2'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == 2


@pytest.mark.asyncio
async def test_films_search_pagination_offset(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    url = f'{URL}/search?query=Cooper&page_size=2&page_number=2'
    async with session.get(url) as resp:
        assert resp.status == HTTPStatus.OK
        json = await resp.json()
        assert len(json) == 1


@pytest.mark.asyncio
async def test_films_field_types(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    url = f'{URL}/'
    async with session.get(url) as resp:
        json = await resp.json()
        for obj in json:
            assert isinstance(obj.get('uuid'), str)
            assert isinstance(obj.get('title'), str)
            assert isinstance(obj.get('imdb_rating'), float)


@pytest.mark.asyncio
async def test_films_execution_time(
        session: aiohttp.ClientSession,
        load_films: list[FilmModel]
):
    start_time = datetime.now()
    url = f'{URL}/'
    async with session.get(url) as resp:
        await resp.json()
        assert resp.status == HTTPStatus.OK
        exec_time = datetime.now() - start_time
        assert exec_time <= timedelta(milliseconds=200)
