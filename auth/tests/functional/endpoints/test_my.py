from jsonschema import validate, Draft202012Validator
import tests.functional.schemas.my as m


URL = '/api/v1/my/'


def test_my_profile(client, jwt_headers, pg_data):
    response = client.get(URL + 'profile')
    assert response.status_code == 401

    response = client.get(URL + 'profile', headers=jwt_headers)
    assert response.status_code == 200
    assert validate(response.json,
                    m.schema_data_user,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_change_password(client, jwt_headers, pg_data):
    response = client.post(URL + 'change_password')
    assert response.status_code == 401

    response = client.post(URL + 'change_password',
                           headers=jwt_headers,
                           json={'password': 'ytrewq321',
                                 'new_password': 'qwerty123',
                                 'new_password_re': 'qwerty123'})

    assert response.status_code == 200
    assert response.json == {'message': 'OK'}


def test_change_email(client, jwt_headers, pg_data):
    response = client.post(URL + 'change_email')
    assert response.status_code == 401

    response = client.post(URL + 'change_email',
                           headers=jwt_headers,
                           json={'email': 'new_email_user@test.com'})

    assert response.status_code == 200
    assert validate(response.json,
                    m.schema_data_user,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_sign_in_history(client, jwt_headers, pg_data):
    response = client.get(URL + 'history')
    assert response.status_code == 401

    response = client.get(URL + 'history', headers=jwt_headers)
    assert response.status_code == 200
    assert validate(response.json,
                    m.schema_history,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_allowed_devices(client, jwt_headers, pg_data):
    response = client.get(URL + 'allowed_devices')
    assert response.status_code == 401

    response = client.get(URL + 'allowed_devices', headers=jwt_headers)
    assert response.status_code == 200
    assert validate(response.json,
                    m.schema_allowed_devices,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None

    response = client.post(URL + 'allowed_devices',
                           headers=jwt_headers,
                           json={'user_agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox'})
    assert response.status_code == 201
    assert len(response.json) == 2
    assert validate(response.json,
                    m.schema_allowed_devices,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None
