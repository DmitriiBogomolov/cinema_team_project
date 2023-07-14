from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_request_id import get_request_id
from async_fastapi_jwt_auth import AuthJWT

from src.api.v1.common import PaginationParams
from src.api.v1.response_models import Film, FilmDetail
from src.services.film import FilmService, get_film_service
from src.core.logger import logger

router = APIRouter()


@router.get('/', response_model=list[Film])
async def film_list(
    pp: PaginationParams = Depends(),
    genre: str = None,
    sort: str = None,
    film_service: FilmService = Depends(get_film_service),
    authorize: AuthJWT = Depends()
) -> list[Film | None]:

    await authorize.jwt_required()

    params = {
        'genre': genre,
        'pp': pp,
        'sort': sort
    }

    films = await film_service.get_list(**params)

    if not films:
        logger.info('films not found!', extra={'request_id': get_request_id()})
        return []

    return [Film(**film.dict()) for film in films]


@router.get('/search', response_model=list[Film])
async def film_search(
    query: str,
    pp: PaginationParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
    authorize: AuthJWT = Depends()
) -> list[Film | None]:

    await authorize.jwt_required()

    params = {
        'query': query,
        'pp': pp
    }
    films = await film_service.get_list(**params)
    if not films:
        logger.info('film not found!', extra={'request_id': get_request_id()})
        return []

    return [Film(**film.dict()) for film in films]


@router.get('/{film_id}', response_model=FilmDetail)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
    authorize: AuthJWT = Depends()
) -> FilmDetail:

    await authorize.jwt_required()

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmDetail(**film.dict())
