from jsonschema import validate, Draft202012Validator
import tests.functional.schemas.roles as r


URL = '/api/v1/roles'


def test_role_list(client, jwt_headers, pg_data):
    response = client.get(URL)
    assert response.status_code == 401

    response = client.get(URL, headers=jwt_headers)
    assert response.status_code == 200
    assert len(response.json) == 5
    assert validate(response.json,
                    r.schema_list_roles,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


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
    print(response.json)
    assert response.status_code == 201
    assert validate(response.json,
                    r.schema_role_output,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_update_role(client, jwt_headers, pg_data):
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
    response = client.patch(
        URL + '/11111169-6712-4666-8116-7c4eaf111111',
        json={
            'name': 'administrator',
            'description': 'do something'
        },
        headers=jwt_headers
    )
    assert response.status_code == 201
    assert validate(response.json,
                    r.schema_role_output,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None
