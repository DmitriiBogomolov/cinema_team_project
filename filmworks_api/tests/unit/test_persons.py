import orjson
from http import HTTPStatus

from fastapi.testclient import TestClient

from .mocks import mock_persons
from src.api.v1.response_models import PersonDetail
from src.api.v1.persons import get_person_service
from src.main import app


class MockPersonService:
    async def get_by_id(self, *args, **kwargs) -> PersonDetail:
        return mock_persons.response_models[0]

    async def get_list(self, *args, **kwargs) -> PersonDetail:
        return mock_persons.response_models


def mock_person_service():
    return MockPersonService()


app.user_middleware.clear()
app.middleware_stack = app.build_middleware_stack()
app.dependency_overrides[get_person_service] = mock_person_service

client = TestClient(app)


def test_get_person_by_id() -> None:
    response = client.get(f'/api/v1/persons/{mock_persons.models[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == orjson.loads(mock_persons.response_models[0].json(by_alias=True))


def test_get_persons_by_list() -> None:
    response = client.get('/api/v1/persons/search')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [orjson.loads(mock.json(by_alias=True)) for mock in mock_persons.response_models]
