from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from async_fastapi_jwt_auth import AuthJWT

from src.api.v1.common import PaginationParams
from src.api.v1.response_models import Film, PersonDetail
from src.services.film import FilmService, get_film_service
from src.services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/search', response_model=list[PersonDetail])
async def persons_search(
    query: str = Query(default='', max_length=100),
    pp: PaginationParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
    authorize: AuthJWT = Depends()
) -> list[PersonDetail | None]:

    await authorize.jwt_required()

    params = {
        'query': query,
        'pp': pp
    }

    persons_list = await person_service.get_list(**params)

    if not persons_list:
        return []

    return [PersonDetail(**person.dict()) for person in persons_list]


@router.get('/{person_id}/film', response_model=list[Film])
async def person_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
    authorize: AuthJWT = Depends()
) -> list[Film | None]:

    await authorize.jwt_required()

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No person with that UUID found.'
        )

    film_ids = [str(film.id) for film in person.films]
    film_list = await film_service.get_list(by_ids=film_ids, sort='imdb_rating')

    if not film_list:
        return []

    return [Film(**film.dict()) for film in film_list]


@router.get('/{person_id}', response_model=PersonDetail)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    authorize: AuthJWT = Depends()
) -> PersonDetail:

    await authorize.jwt_required()

    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No person with that UUID found.'
        )
    return PersonDetail(**person.dict())
