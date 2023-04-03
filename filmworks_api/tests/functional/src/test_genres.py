from datetime import datetime, timedelta
from http import HTTPStatus

import pytest

from src.models.genre import Genre as GenreModel

from ..testdata.mocks.mock_genres import ResponseGenreModel

URL = 'genres'

pytestmark = pytest.mark.asyncio


async def test_genre_not_found(
    make_get_request,
    clear_genres: None
):

    url = f'/{URL}/05fb2223-dabf-40e9-9924-20446fadf39'
    response = await make_get_request(url)
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body.get('detail') == 'No genre with that UUID found.'


async def test_genre_by_id(
    make_get_request,
    load_genres: list[GenreModel]
):

    genre = load_genres[0]
    url = f'/{URL}/{genre.id}'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert response.body == ResponseGenreModel(**genre.dict()).get_json()


async def test_genres_list(
    make_get_request,
    load_genres: list[GenreModel]
):

    sorted_genres = sorted(load_genres, key=lambda x: x.name)
    url = f'/{URL}/'
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == len(sorted_genres)
    assert response.body == [
        ResponseGenreModel(**genre.dict()).get_json() for genre in sorted_genres]


async def test_genres_field_types(
    make_get_request,
    load_genres: list[GenreModel]
):

    url = f'/{URL}/'
    response = await make_get_request(url)

    for obj in response.body:
        assert isinstance(obj.get('uuid'), str)
        assert isinstance(obj.get('name'), str)


async def test_genres_execution_time(
    make_get_request,
    load_genres: list[GenreModel]
):

    start_time = datetime.now()
    url = f'/{URL}/'
    response = await make_get_request(url)
    exec_time = datetime.now() - start_time

    assert response.status == HTTPStatus.OK
    assert exec_time <= timedelta(milliseconds=200)
