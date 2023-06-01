import tests.functional.references.roles as r
from tests.functional.helpers import clear


URL = '/api/v1/roles'


def test_role_list(client, jwt_headers, pg_data):
    response = client.get(URL)
    assert response.status_code == 401

    response = client.get(URL, headers=jwt_headers)
    assert response.status_code == 200
    assert len(response.json) == len(r.role_list_output)
    assert response.json == r.role_list_output


def test_create_role(client, jwt_headers, pg_data):
    response = client.post(URL)
    assert response.status_code == 401
    response = client.post(
        URL,
        json={
            'name': 'moderator',
            'description': 'do something'
        },
        headers=jwt_headers
    )
    assert response.status_code == 201
    assert clear(response.json) == clear(r.create_role_output)
