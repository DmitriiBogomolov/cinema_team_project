import json

import httpx
import pytest
from mocks import mock_genres


@pytest.mark.anyio
async def test_get_genres_by_id(client: httpx.AsyncClient) -> None:

    response = await client.get(f'/api/v1/genres/{mock_genres.list_[0].id}')

    assert response.status_code == 200
    assert response.json() == json.loads(mock_genres.list_[0].json(by_alias=True, exclude={'description'}))


@pytest.mark.anyio
async def test_get_persons_by_list(client: httpx.AsyncClient) -> None:
    response = await client.get('/api/v1/genres/')
    assert response.status_code == 404
