import requests

from sqlalchemy.orm import Session

from tests.functional.config import test_config
from tests.functional.sent_data import (
    default_event,
    manual_mailing
)


HOST = test_config.api_url
HEADERS = {
    'Authorization': f'Bearer {test_config.test_token}'
}


def test_default(init_pg: Session):
    """Тестирует сценарий, обрабатываемый типовым хендлером"""
    URL = HOST

    response = requests.post(URL, json=default_event['valid'])
    assert response.status_code == 401

    response = requests.get(
        URL, headers=HEADERS
    )
    assert response.status_code == 405

    response = requests.put(
        URL, json=default_event['valid'], headers=HEADERS
    )
    assert response.status_code == 405

    response = requests.patch(
        URL, json=default_event['valid'], headers=HEADERS
    )
    assert response.status_code == 405

    response = requests.head(
        URL, headers=HEADERS
    )
    assert response.status_code == 405

    for data in default_event['invalid']:
        response = requests.post(
            URL, json=data, headers=HEADERS
        )
        assert response.status_code == 422

    response = requests.post(
        URL, json=default_event['valid'], headers=HEADERS
    )
    assert response.status_code == 200
    response.json == {'message': 'OK'}


def test_manual_mailing(init_pg: Session):
    """Тестирует сценарий ручной рассылки"""
    URL = f'{HOST}/send_manual'

    response = requests.post(URL, json=manual_mailing['valid'])
    assert response.status_code == 401

    response = requests.get(
        URL, headers=HEADERS
    )
    assert response.status_code == 405

    response = requests.put(
        URL, json=manual_mailing['valid'], headers=HEADERS
    )
    assert response.status_code == 405

    response = requests.patch(
        URL, json=manual_mailing['valid'], headers=HEADERS
    )
    assert response.status_code == 405

    response = requests.head(
        URL, headers=HEADERS
    )
    assert response.status_code == 405

    for data in manual_mailing['invalid']:
        response = requests.post(
            URL, json=data, headers=HEADERS
        )
        assert response.status_code == 422

    response = requests.post(
        URL, json=manual_mailing['valid'], headers=HEADERS
    )
    assert response.status_code == 200
    response.json == {'message': 'OK'}
