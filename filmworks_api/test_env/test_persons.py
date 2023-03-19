import json

import httpx
import pytest
from mocks import mock_persons


@pytest.mark.anyio
async def test_get_person_by_id(client: httpx.AsyncClient) -> None:

    response = await client.get(f'/api/v1/persons/{mock_persons.list_[0].id}')

    assert response.status_code == 200
    assert response.json() == json.loads(mock_persons.list_[0].json(by_alias=True))


@pytest.mark.anyio
async def test_get_persons_by_list(client: httpx.AsyncClient) -> None:
    response = await client.get('/api/v1/persons/search?query=Person&page_number=1&page_size=50')
    assert response.status_code == 404
