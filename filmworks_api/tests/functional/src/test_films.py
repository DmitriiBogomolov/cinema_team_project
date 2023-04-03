from datetime import datetime, timedelta
from http import HTTPStatus

import pytest

from src.models.film import Filmwork as FilmModel

from ..testdata.mocks.mock_films import ResponseFilmDetailModel, ResponseFilmModel, FILMS_LIST

URL = 'films'

pytestmark = pytest.mark.asyncio


async def test_film_not_found(
    make_get_request,
    clear_films: None
):
    url = f'/{URL}/3fa85f64-5717-4562-b3fc-2c963f66afa7'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body.get('detail') == 'film not found'


async def test_films_not_found(
    make_get_request,
    clear_films: None
):
    url = f'/{URL}/'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert response.body == []


async def test_film_by_id(
    make_get_request,
    load_films: list[FilmModel]
):
    film = load_films[0]
    url = f'/{URL}/{film.id}'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert response.body == ResponseFilmDetailModel(**film.dict()).get_json()


async def test_films_list(
    make_get_request,
    load_films: list[FilmModel]
):
    sorted_films = sorted(load_films, key=lambda x: x.imdb_rating, reverse=True)
    url = f'/{URL}/?sort=-imdb_rating'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(FILMS_LIST)
    assert response.body == [
        ResponseFilmModel(**film.dict()).get_json() for film in sorted_films]


async def test_films_list_pagination(
    make_get_request,
    load_films: list[FilmModel]
):
    url = f'/{URL}/?sort=-imdb_rating&page_size=3'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 3


async def test_films_list_pagination_offset(
    make_get_request,
    load_films: list[FilmModel]
):
    url = f'/{URL}/?sort=-imdb_rating&page_size=4&page_number=3'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1


async def test_films_by_genre(
    make_get_request,
    load_films: list[FilmModel]
):
    sorted_films = sorted(load_films[:5], key=lambda x: x.imdb_rating, reverse=True)
    url = f'/{URL}/?genre=120a21cf-9097-479e-904a-13dd7198c1dd&sort=-imdb_rating'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 5
    assert response.body == [
        ResponseFilmModel(**film.dict()).get_json() for film in sorted_films]


async def test_films_search(
    make_get_request,
    load_films: list[FilmModel]
):
    url = f'/{URL}/search?query=Cooper'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 3


async def test_films_search_pagination(
    make_get_request,
    load_films: list[FilmModel]
):
    url = f'/{URL}/search?query=Cooper&page_size=2'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 2


async def test_films_search_pagination_offset(
    make_get_request,
    load_films: list[FilmModel]
):
    url = f'/{URL}/search?query=Cooper&page_size=2&page_number=2'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1


@pytest.mark.asyncio
async def test_films_field_types(
    make_get_request,
    load_films: list[FilmModel]
):
    url = f'/{URL}/'
    response = await make_get_request(url)

    for obj in response.body:
        assert isinstance(obj.get('uuid'), str)
        assert isinstance(obj.get('title'), str)
        assert isinstance(obj.get('imdb_rating'), float)


@pytest.mark.asyncio
async def test_films_execution_time(
    make_get_request,
    load_films: list[FilmModel]
):
    start_time = datetime.now()
    url = f'/{URL}/'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    exec_time = datetime.now() - start_time
    assert exec_time <= timedelta(milliseconds=200)
