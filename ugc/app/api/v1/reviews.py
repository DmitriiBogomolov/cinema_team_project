"""Эндпоинты для работы с рецензиями фильмов"""

from http import HTTPStatus
from uuid import UUID

from fastapi import (
    APIRouter, Depends, status,
    Response, HTTPException
)
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.request_models import (
    RequestReviewModel, RequestLikeModel
)
from app.models import ReviewModel, LikeModel
from app.repositories.reviews import (
    AbstractReviewsRepository,
    get_reviews_repository
)
from app.repositories.reviews_likes import (
    ReviewsLikesRepository,
    get_reviews_likes_repository
)
from app.repositories.zcommon import SortParam
from app.core.jwt import authorize_for_roles


router = APIRouter()


@router.get('', response_model=list[ReviewModel])
async def get_movie_reviews(
    movie_id: UUID,
    sort: SortParam = Depends(),
    auth: AuthJWT = Depends(),
    reviews_repository: AbstractReviewsRepository = (
        Depends(get_reviews_repository)
    )
) -> list[ReviewModel | None]:
    """Возвращает список рецензий фильма"""
    await authorize_for_roles(auth)

    reviews = await \
        reviews_repository.get_list_for_movie(
            movie_id,
            sort=sort
        )
    if not reviews:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )
    return reviews


@router.post('')
async def post_movie_review(
    reuqest_review: RequestReviewModel,
    auth: AuthJWT = Depends(),
    reviews_repository: AbstractReviewsRepository = (
        Depends(get_reviews_repository)
    )
) -> JSONResponse:
    """Добавляет рецензию текущего пользователя к фильму"""
    current_user = await authorize_for_roles(auth)

    review = ReviewModel(
        movie_id=reuqest_review.movie_id,
        user_id=current_user['id'],
        text=reuqest_review.text
    )
    result = await reviews_repository.add(review)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': result.target_id}
    )


@router.get(
    '/{review_id}/likes',
    response_model=list[LikeModel]
)
async def get_review_likes(
    review_id: UUID,
    auth: AuthJWT = Depends(),
    likes_repository: ReviewsLikesRepository = (
        Depends(get_reviews_likes_repository)
    )
) -> list[LikeModel | None]:
    """Получает список оценок (лайков) рецензии"""
    await authorize_for_roles(auth)

    return await \
        likes_repository.get_list(review_id)


@router.post('/{review_id}/like')
async def post_review_like(
    review_id: UUID,
    request_like: RequestLikeModel,
    auth: AuthJWT = Depends(),
    likes_repository: ReviewsLikesRepository = (
        Depends(get_reviews_likes_repository)
    )
) -> JSONResponse:
    """Добавляет оценку (лай) текущего пользователя к рецензии"""
    current_user = await authorize_for_roles(auth)

    like = LikeModel(
        entity_id=review_id,
        user_id=current_user['id'],
        rating=request_like.rating
    )
    result = await likes_repository.add(like)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': str(result.target_id)}
    )


@router.delete(
    '/{review_id}/like',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_review_like(
    review_id: UUID,
    auth: AuthJWT = Depends(),
    likes_repository: ReviewsLikesRepository = (
        Depends(get_reviews_likes_repository)
    )
) -> JSONResponse:
    """
    Удаляет оценку (лайк) рецензии,
    если он пренадлежит текущему пользователю
    """
    current_user = await authorize_for_roles(auth)

    result = await (
        likes_repository.delete_for_user(
            review_id,
            current_user['id']
        )
    )
    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )
