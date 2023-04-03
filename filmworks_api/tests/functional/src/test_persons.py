from http import HTTPStatus

import pytest

from tests.functional.testdata.mocks.mock_persons import TEST_PERSONS, RESPONSE_REFS

URL = 'persons'

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('person_id, expected_status', [
    ('ffffffff-ffff-ffff-ffff-ffffffffffff', HTTPStatus.NOT_FOUND),
    (TEST_PERSONS[0]['id'], HTTPStatus.OK),
])
async def test_get_person_status(
    person_id,
    expected_status,
    load_persons,
    make_get_request
):
    url = f"""/{URL}/{person_id}"""
    response = await make_get_request(url)

    assert response.status == expected_status


async def test_get_person_by_correct_uuid_returns_correct_data(
    make_get_request,
    load_persons
):
    url = f"""/{URL}/{TEST_PERSONS[0]['id']}"""
    response = await make_get_request(url)

    assert response.body == RESPONSE_REFS['response_ref']


async def test_get_person_films(
    make_get_request,
    load_persons,
    load_films
):
    url = f"""/{URL}/{TEST_PERSONS[0]['id']}/film"""
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 3
    assert response.body == RESPONSE_REFS['films_ref']


async def test_person_search(
    make_get_request,
    load_persons
):
    url = f"""/{URL}/search?query=Aaron"""
    response = await make_get_request(url)

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 6


@pytest.mark.parametrize('page_size, page_number, expected_length, expected_status', [
    (5, None, 5, HTTPStatus.OK),
    (5, 2, 1, HTTPStatus.OK),
    (-10, 2, 1, HTTPStatus.UNPROCESSABLE_ENTITY),
])
async def test_person_search_pagination(
    make_get_request,
    load_persons,
    page_size,
    page_number,
    expected_length,
    expected_status
):
    url = f"""/{URL}/search?query=Aaron"""
    if page_size:
        url += f'&page_size={page_size}'
    if page_number:
        url += f'&page_number={page_number}'
    response = await make_get_request(url)

    assert response.status == expected_status
    assert len(response.body) == expected_length
