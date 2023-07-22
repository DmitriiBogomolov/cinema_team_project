from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.unit.mocks.view_events_mocks import EVENT_MOCKS
from tests.config import test_settings
from app.api.v1.views import get_kafka_producer
from app.api.v1.views import get_redis
from app.main import app


token = test_settings.test_token


class MockKafkaProducer:
    async def send_and_wait(self, *args, **kwargs) -> None:
        return None


class MockRedis:
    async def set(self, *args, **kwargs) -> None:
        return None


def mock_kafka_producer():
    return MockKafkaProducer()


def mock_redis():
    return MockRedis()


app.user_middleware.clear()
app.middleware_stack = app.build_middleware_stack()
app.dependency_overrides[get_kafka_producer] = mock_kafka_producer
app.dependency_overrides[get_redis] = mock_redis


client = TestClient(app)


def test_views_get() -> None:
    response = client.get('/api/v1/views')
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_views_post() -> None:
    response = client.post(
        '/api/v1/views',
        json=EVENT_MOCKS['correct']
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    for case in EVENT_MOCKS:
        response = client.post(
            '/api/v1/views',
            headers={'Authorization': f'Bearer {token}'},
            json=EVENT_MOCKS[case]
        )

        match case:
            case 'correct':
                target = HTTPStatus.OK
            case 'no_movie_id':
                target = HTTPStatus.UNPROCESSABLE_ENTITY
            case 'no_duration':
                target = HTTPStatus.UNPROCESSABLE_ENTITY
            case 'no_lenght_movie':
                target = HTTPStatus.UNPROCESSABLE_ENTITY
            case 'incorrect_movie_id':
                target = HTTPStatus.UNPROCESSABLE_ENTITY
            case 'duration_out_of_range':
                target = HTTPStatus.UNPROCESSABLE_ENTITY
            case 'lenght_movie_out_of_range':
                target = HTTPStatus.UNPROCESSABLE_ENTITY
            case 'icorrect_duration':
                target = HTTPStatus.UNPROCESSABLE_ENTITY

        assert response.status_code == target
