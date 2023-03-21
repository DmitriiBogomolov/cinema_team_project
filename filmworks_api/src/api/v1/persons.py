from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, Query

from src.api.v1.response_models import PersonDetail
from src.core.config import pit_config
from src.services.person import PersonService, get_person_service
from src.services.point_in_time import PITService, get_pit_service

router = APIRouter()

INDEX_NAME = 'persons'


@router.get('/search', response_model=list[PersonDetail])
async def get_persons_list(
    response: Response,
    query: str = Query(default='', max_length=100),
    page_number: int = Query(default=1, min=1),
    page_size: int = Query(default=50, min=1, max=200),
    person_list_PIT: str | None = Cookie(default=None),
    person_service: PersonService = Depends(get_person_service),
    PIT_service: PITService = Depends(get_pit_service)
) -> list[PersonDetail]:

    if not person_list_PIT:
        person_list_PIT = await PIT_service.get_pit_token(INDEX_NAME)

    response.set_cookie(key='person_list_PIT', value=person_list_PIT, max_age=pit_config.PIT_MAX_AGE)

    params = {
        'query': query,
        'page_number': page_number,
        'page_size': page_size,
        'pit': person_list_PIT
    }

    persons_list = await person_service.get_list(**params)

    if not persons_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No such persons.'
        )
    return [PersonDetail(**person.dict()) for person in persons_list]


@router.get('/{person_id}', response_model=PersonDetail)
async def get_person_details(
    person_id: UUID,
    person_service: PersonService = Depends(get_person_service)
) -> PersonDetail:

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No person with that UUID found.'
        )
    return PersonDetail(**person.dict())
