"""
Эндпоинты для работы с закладками
(сохраненными фильмами) пользователя
"""

from http import HTTPStatus
from uuid import UUID

from fastapi import (
    APIRouter, Depends, status, Response
)
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.request_models import (
    RequestBookmarkModel
)
from app.models import BookmarkModel
from app.repositories.bookmarks import (
    get_bookmark_repository,
    AbstractBookmarkRepository
)
from app.core.jwt import authorize_for_roles


router = APIRouter()


@router.get('', response_model=list[BookmarkModel])
async def get_bookmarks(
    auth: AuthJWT = Depends(),
    repository: AbstractBookmarkRepository = (
        Depends(get_bookmark_repository)
    )
) -> list[BookmarkModel | None]:
    """Возвращает закладки текущего пользоваетля"""
    current_user = await authorize_for_roles(auth)

    return await \
        repository.get_list_for_user(
            current_user['id']
        )


@router.post('')
async def post_bookmark(
    request_bookmark: RequestBookmarkModel,
    auth: AuthJWT = Depends(),
    repository: AbstractBookmarkRepository = (
        Depends(get_bookmark_repository)
    )
) -> JSONResponse:
    """Добавляет закладку текущему пользователю"""
    current_user = await authorize_for_roles(auth)

    bookmark = BookmarkModel(
        user_id=current_user['id'],
        movie_id=request_bookmark.movie_id
    )
    result = await repository.add(bookmark)
    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': result.target_id}
    )


@router.delete(
    '/{bookmark_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_bookmark(
    bookmark_id: UUID,
    auth: AuthJWT = Depends(),
    repository: AbstractBookmarkRepository = (
        Depends(get_bookmark_repository)
    )
) -> JSONResponse:
    """
    Удаляет закладку
    если она пренадлежит текущему пользователю
    """
    current_user = await authorize_for_roles(auth)
    await repository.delete_for_user(
        bookmark_id,
        current_user['id']
    )
