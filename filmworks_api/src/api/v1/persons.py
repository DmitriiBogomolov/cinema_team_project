from http import HTTPStatus

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, Query

from src.api.v1.common import PaginationParams
from src.api.v1.response_models import PersonDetail, Film
from src.core.config import pit_config
from src.services.person import PersonService, get_person_service
from src.services.film import FilmService, get_film_service
from src.services.point_in_time import PITService, get_pit_service

router = APIRouter()

INDEX_NAME = 'persons'


@router.get('/search', response_model=list[PersonDetail])
async def get_persons_list(
    response: Response,
    query: str = Query(default='', max_length=100),
    pp: PaginationParams = Depends(),
    person_list_PIT: str | None = Cookie(default=None),
    person_service: PersonService = Depends(get_person_service),
    PIT_service: PITService = Depends(get_pit_service)
) -> list[PersonDetail]:

    if not person_list_PIT:
        person_list_PIT = await PIT_service.get_pit_token(INDEX_NAME)

    response.set_cookie(key='person_list_PIT', value=person_list_PIT, max_age=pit_config.PIT_MAX_AGE)

    params = {
        'query': query,
        'pp': pp,
        'pit': person_list_PIT
    }

    persons_list = await person_service.get_list(**params)

    if not persons_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No such persons.'
        )
    return [PersonDetail(**person.dict()) for person in persons_list]


@router.get('/{person_id}/film', response_model=list[Film])
async def get_person_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service)
) -> Film:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No person with that UUID found.'
        )

    film_ids = [str(film.id) for film in person.films]
    film_list = await film_service.get_by_ids(film_ids)

    if not film_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='There are no films associated with this person id.'
        )
    return [Film(**film.dict()) for film in film_list]


@router.get('/{person_id}', response_model=PersonDetail)
async def get_person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service)
) -> PersonDetail:

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No person with that UUID found.'
        )
    return PersonDetail(**person.dict())
