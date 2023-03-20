import orjson
from fastapi.testclient import TestClient

from api.v1.films import get_film_service
from api.v1.response_models import FilmDetail
from models.film import Filmwork
from main import app

mock_filmwork = Filmwork(
    id='5633f23a-9423-4c8e-81d9-584d9a402aeb',
    title='Mock Filmwork',
    imdb_rating=9.7,
    description=None,
    genres=[],
    actors=[],
    directors=[],
    writers=[],
)

mock_response = FilmDetail(**mock_filmwork.dict())


class MockFilmService:
    async def get_by_id(self, *args, **kwargs) -> Filmwork:
        return mock_filmwork


def mock_film_service():
    return MockFilmService()


app.user_middleware.clear()
app.middleware_stack = app.build_middleware_stack()
app.dependency_overrides[get_film_service] = mock_film_service


client = TestClient(app)


def test_get_film_by_id():
    response = client.get('/api/v1/films/5633f23a-9423-4c8e-81d9-584d9a402aeb')
    assert response.status_code == 200
    assert response.json() == orjson.loads(mock_response.json(by_alias=True))
