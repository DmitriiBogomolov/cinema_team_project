from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from src.services.film import FilmService, get_film_service
from src.api.v1.response_models import Film, FilmDetail

router = APIRouter()


@router.get('', response_model=list[Film])
async def film_list(
    genre: str = None,
    sort: str = None,
    page_size: int = 50,
    page_number: int = 1,
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_list([
        genre,
        sort,
        page_size,
        page_number
    ])
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    return [Film(**film.dict()) for film in films]


@router.get('/search', response_model=list[Film])
async def film_search(
    query: str,
    page_size: int = 50,
    page_number: int = 1,
    film_service: FilmService = Depends(get_film_service)
) -> list[Film]:

    films = await film_service.get_search_list([
        query,
        page_size,
        page_number
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
