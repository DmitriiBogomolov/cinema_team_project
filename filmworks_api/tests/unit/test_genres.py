import orjson
from http import HTTPStatus

from fastapi.testclient import TestClient

from .mocks import mock_genres
from src.api.v1.genres import get_genre_service
from src.api.v1.response_models import Genre
from src.main import app


class MockGenreService:
    async def get_by_id(self, *args, **kwargs) -> Genre:
        return mock_genres.response_models[0]

    async def get_list(self, *args, **kwargs) -> Genre:
        return mock_genres.response_models


def mock_genre_service():
    return MockGenreService()


app.user_middleware.clear()
app.middleware_stack = app.build_middleware_stack()
app.dependency_overrides[get_genre_service] = mock_genre_service


client = TestClient(app)


def test_get_genre_by_id() -> None:
    response = client.get(f'/api/v1/genres/{mock_genres.models[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == orjson.loads(mock_genres.response_models[0].json(exclude={'description'}, by_alias=True))


def test_get_genres_by_list() -> None:
    response = client.get('/api/v1/genres/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [orjson.loads(mock.json(exclude={'description'}, by_alias=True))
                               for mock in mock_genres.response_models]
