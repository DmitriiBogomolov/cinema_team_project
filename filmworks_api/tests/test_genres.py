import orjson

from fastapi.testclient import TestClient

from mocks import mock_genres
from api.v1.genres import get_genre_service
from main import app


class MockGenreService:
    async def get_by_id(self, *args, **kwargs) -> mock_genres.Genre:
        return mock_genres.list_[0]

    async def get_list(self, *args, **kwargs) -> mock_genres.Genre:
        return mock_genres.list_


def mock_genre_service():
    return MockGenreService()


app.user_middleware.clear()
app.middleware_stack = app.build_middleware_stack()
app.dependency_overrides[get_genre_service] = mock_genre_service


client = TestClient(app)


def test_get_genre_by_id() -> None:
    response = client.get(f'/api/v1/genres/{mock_genres.list_[0].uuid}')
    assert response.status_code == 200
    assert response.json() == orjson.loads(mock_genres.list_[0].json(exclude={'description'}))


def test_get_genres_by_list() -> None:
    response = client.get('/api/v1/genres/')
    assert response.status_code == 200
    assert response.json() == [orjson.loads(mock.json(exclude={'description'})) for mock in mock_genres.list_]
