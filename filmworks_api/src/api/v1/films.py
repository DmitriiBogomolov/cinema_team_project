from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.common import PaginationParams
from src.api.v1.response_models import Film, FilmDetail
from src.services.film import FilmService, get_film_service

router = APIRouter()


@router.get('/', response_model=list[Film])
async def film_list(
    pp: PaginationParams = Depends(PaginationParams),
    genre: str = None,
    sort: str = None,
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_list([
        genre,
        sort,
        pp.page_size,
        pp.page_number
    ])
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [Film(**film.dict()) for film in films]


@router.get('/search', response_model=list[Film])
async def film_search(
    query: str,
    pp: PaginationParams = Depends(PaginationParams),
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_search_list([
        query,
        pp.page_size,
        pp.page_number
    ])
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [Film(**film.dict()) for film in films]


@router.get('/{film_id}', response_model=FilmDetail)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmDetail(**film.dict())
