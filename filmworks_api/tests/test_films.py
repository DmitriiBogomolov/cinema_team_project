from filmworks_api.src.api.v1.films import Film, get_film_service
from fastapi.testclient import TestClient
from filmworks_api.src.main import app


mock_filmwork = Film(
    uuid='5633f23a-9423-4c8e-81d9-584d9a402aeb',
    title='Mock Filmwork',
    imdb_rating=9.7
)


class MockFilmService:
    async def get_by_id(self, *args, **kwargs) -> Film:
        return mock_filmwork


def mock_film_service():
    return MockFilmService()


app.dependency_overrides[get_film_service] = mock_film_service

client = TestClient(app)


def test_get_film_by_id():
    response = client.get('/api/v1/films/5633f23a-9423-4c8e-81d9-584d9a402aeb')
    assert response.status_code == 200
    assert response.json() == mock_filmwork.dict()
