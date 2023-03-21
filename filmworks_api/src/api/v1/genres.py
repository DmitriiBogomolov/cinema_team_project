from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.response_models import Genre
from src.services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/{genre_id}', response_model=Genre)
async def get_genre_details(
    genre_id: UUID,
    genre_service: GenreService = Depends(get_genre_service)
) -> Genre:

    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No genre with that UUID found.'
        )
    return Genre(**genre.dict())


@router.get('/', response_model=list[Genre])
async def get_genres_list(
    genre_service: GenreService = Depends(get_genre_service)
) -> list[Genre]:

    genres_list = await genre_service.get_list()
    if not genres_list:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No any genres.'
        )
    return [Genre(**genre.dict()) for genre in genres_list]
