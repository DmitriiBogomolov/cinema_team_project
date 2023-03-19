import json

from fastapi.testclient import TestClient

from mocks import mock_persons
from api.v1.persons import get_person_service, get_pit_service
from main import app


class MockPersonService:
    async def get_by_id(self, *args, **kwargs) -> mock_persons.Person:
        return mock_persons.list_[0]

    async def get_list(self, *args, **kwargs) -> mock_persons.Person:
        return mock_persons.list_


class MockPitService:
    async def get_pit_token(self, *args, **kwargs) -> None:
        pass


def mock_pit_service():
    return MockPitService()


def mock_person_service():
    return MockPersonService()


app.user_middleware.clear()
app.middleware_stack = app.build_middleware_stack()
app.dependency_overrides[get_person_service] = mock_person_service
app.dependency_overrides[get_pit_service] = mock_pit_service


client = TestClient(app)


def test_get_person_by_id() -> None:
    response = client.get(f'/api/v1/persons/{mock_persons.list_[0].uuid}')
    assert response.status_code == 200
    assert response.json() == json.loads(mock_persons.list_[0].json())


def test_get_persons_by_list() -> None:
    response = client.get('/api/v1/persons/search')
    assert response.status_code == 200
    assert response.json() == [json.loads(mock.json()) for mock in mock_persons.list_]
