"""Эндпоинты для работы с лайками (оценками) фильмов"""

from http import HTTPStatus
from uuid import UUID

from fastapi import (
    APIRouter, Depends, status,
    Response, HTTPException
)
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.request_models import RequestLikeModel
from app.models import LikeModel
from app.repositories.movies_likes import (
    AbstractMoviesLikesRepository,
    get_movies_likes_repository
)
from app.core.jwt import authorize_for_roles


router = APIRouter()


@router.get(
    '/{movie_id}/likes',
    response_model=list[LikeModel]
)
async def get_movie_likes(
    movie_id: UUID,
    auth: AuthJWT = Depends(),
    repository: AbstractMoviesLikesRepository = (
        Depends(get_movies_likes_repository)
    )
) -> list[LikeModel | None]:
    """Возвращает список лайков (оценок) фильма"""
    await authorize_for_roles(auth)
    return await repository.get_list(movie_id)


@router.get('/{movie_id}/likes/count')
async def get_movie_likes_count(
    movie_id: UUID,
    auth: AuthJWT = Depends(),
    repository: AbstractMoviesLikesRepository = (
        Depends(get_movies_likes_repository)
    )
) -> JSONResponse:
    """Возвращает количество лайков (оценок) фильма"""
    await authorize_for_roles(auth)

    count = await repository.get_count(movie_id)

    if not count:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'count': count}
    )


@router.get('/{movie_id}/likes/average')
async def get_movie_likes_average(
    movie_id: UUID,
    auth: AuthJWT = Depends(),
    repository: AbstractMoviesLikesRepository = (
        Depends(get_movies_likes_repository)
    )
) -> list[LikeModel | None]:
    """Возвращает среднее значение оценок фильма"""
    await authorize_for_roles(auth)

    average = await (
        repository.get_average_rating(movie_id)
    )

    if average == -1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'average': average}
    )


@router.post('/{movie_id}/likes')
async def post_movie_like(
    movie_id: UUID,
    request_like: RequestLikeModel,
    auth: AuthJWT = Depends(),
    repository: AbstractMoviesLikesRepository = (
        Depends(get_movies_likes_repository)
    )
) -> JSONResponse:
    """Добавляет лайк (оценку) фильму от текущего пользователя"""
    current_user = await authorize_for_roles(auth)

    like = LikeModel(
        entity_id=movie_id,
        user_id=current_user['id'],
        rating=request_like.rating
    )

    result = await repository.add(like)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': result.target_id}
    )


@router.delete(
    '/{movie_id}/like',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_movie_like(
    movie_id: UUID,
    auth: AuthJWT = Depends(),
    repository: AbstractMoviesLikesRepository = (
        Depends(get_movies_likes_repository)
    )
) -> JSONResponse:
    """
    Удаляет лайк (оценку) фильма
    если он пренадлежит текущему пользователю
    """
    current_user = await authorize_for_roles(auth)

    result = await repository.delete_for_user(
        movie_id, current_user['id']
    )

    if not result.count:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )
