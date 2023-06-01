from jsonschema import validate, Draft202012Validator
import tests.functional.schemas.users as u


URL = '/api/v1/users/11111169-6712-4666-8116-7c4eaf111111'


def test_get_user(client, jwt_headers, pg_data):
    response = client.get(URL)
    assert response.status_code == 401

    response = client.get(URL, headers=jwt_headers)
    assert response.status_code == 200
    assert validate(response.json,
                    u.schema_user_output,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_user_update(client, jwt_headers, pg_data):
    response = client.patch(URL)
    assert response.status_code == 401
    response = client.patch(
        URL,
        json={
            'email': 'new_email@email.com'
        },
        headers=jwt_headers
    )
    assert response.status_code == 200
    assert validate(response.json,
                    u.schema_user_output,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_user_set_role(client, jwt_headers, pg_data):
    response = client.post(URL + '/roles/22222269-6712-4666-8116-7c4eaf222222')
    assert response.status_code == 401
    response = client.post(
        URL + '/roles/22222269-6712-4666-8116-7c4eaf222222',
        headers=jwt_headers
    )
    assert response.status_code == 200
    assert len(response.json['roles']) == 2
    assert validate(response.json,
                    u.schema_user_output,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_user_revoke_role(client, jwt_headers, pg_data):
    response = client.delete(URL + '/roles/11111169-6712-4666-8116-7c4eaf111111')
    assert response.status_code == 401
    response = client.delete(
        URL + '/roles/11111169-6712-4666-8116-7c4eaf111111',
        headers=jwt_headers
    )
    assert response.status_code == 200
    assert len(response.json['roles']) == 0
    assert validate(response.json, u.schema_user_output, format_checker=Draft202012Validator.FORMAT_CHECKER) == None
