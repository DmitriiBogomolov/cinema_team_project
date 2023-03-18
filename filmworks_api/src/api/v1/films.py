from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from services.film import FilmService, get_film_service
from .response_models import Film, FilmDetail, Genre, Person

router = APIRouter()


@router.get('', response_model=List[Film])
async def film_list(
    genre: str = None,
    sort: str = None,
    page_size: int = 50,
    page_number: int = 1,
    film_service: FilmService = Depends(get_film_service)
) -> List[Film]:

    films = await film_service.get_list([
        genre,
        sort,
        page_size,
        page_number
    ])
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    movies = []
    for film in films:
        movies.append(Film(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            ))
    return movies


@router.get('/search', response_model=List[Film])
async def film_search(
    query: str,
    page_size: int = 50,
    page_number: int = 1,
    film_service: FilmService = Depends(get_film_service)
) -> List[Film]:

    films = await film_service.get_search_list([
        query,
        page_size,
        page_number
    ])
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    movies = []
    for film in films:
        movies.append(Film(
            uuid=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
            ))
    return movies


@router.get('/{film_id}', response_model=FilmDetail)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:

    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return FilmDetail(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=[Genre(uuid=g.id, name=g.name) for g in film.genres],
        actors=[Person(uuid=p.id, full_name=p.name) for p in film.actors],
        writers=[Person(uuid=p.id, full_name=p.name) for p in film.writers],
        directors=[Person(uuid=p.id, full_name=p.name) for p in film.directors],
        )
