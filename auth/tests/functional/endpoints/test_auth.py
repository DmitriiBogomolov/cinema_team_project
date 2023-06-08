from jsonschema import validate, Draft202012Validator
import tests.functional.schemas.my as m


URL = '/api/v1/'


def login_user(client):
    response = client.post(URL + 'login', auth=('111@email.com', 'ytrewq321'))
    refresh_token = response.json['refresh']
    headers = {
        'Authorization': 'Bearer {}'.format(refresh_token)
    }
    return headers


def test_register(client, pg_data):
    response = client.post(URL + 'register',
                           json={'email': 'new_user@test.com', 'password': 'ytrewq321'})
    assert response.status_code == 201
    assert validate(response.json,
                    m.schema_data_user,
                    format_checker=Draft202012Validator.FORMAT_CHECKER) == None


def test_login(client, pg_data):
    response = client.post(URL + 'login', auth=('111@email.com', 'ytrewq321'))

    assert response.status_code == 200
    assert list(response.json.keys()) == ['access', 'refresh']


def test_refresh(client, pg_data):
    response = client.post(URL + 'refresh', headers=login_user(client))

    assert response.status_code == 200
    assert list(response.json.keys()) == ['access', 'refresh']
