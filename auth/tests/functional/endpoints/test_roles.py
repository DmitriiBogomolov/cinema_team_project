def test_role_list(client, pg_data):
    response = client.get('/api/v1')
    assert b'hello' in response.data
