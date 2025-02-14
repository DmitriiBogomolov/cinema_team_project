from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from async_fastapi_jwt_auth import AuthJWT

from src.api.v1.response_models import Genre
from src.services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get('/', response_model=list[Genre])
async def genres_list(
    genre_service: GenreService = Depends(get_genre_service),
    authorize: AuthJWT = Depends()
) -> list[Genre | None]:

    await authorize.jwt_required()

    genres = await genre_service.get_list()
    if not genres:
        return []

    return [Genre(**genre.dict()) for genre in genres]


@router.get('/{genre_id}', response_model=Genre)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
    authorize: AuthJWT = Depends()
) -> Genre:

    await authorize.jwt_required()

    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No genre with that UUID found.'
        )
    return Genre(**genre.dict())
