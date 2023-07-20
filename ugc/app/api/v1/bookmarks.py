import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response, HTTPException
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.request_models import BookmarkRequestModel
from app.models import BookmarkModel
from app.core.jwt import access_check
from app.services.repository import MongoRepository, get_mongo_repository


router = APIRouter()


@router.get('', response_model=list[BookmarkModel])
async def get_bookmarks(
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> list[BookmarkModel | None]:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())
    search = {'user_id': str(current_user['id'])}
    docs = await mongo.find(
        'bookmarks', search, [('created_at', -1)]
    )
    return [BookmarkModel(**doc)
            for doc in docs]


@router.post('')
async def post_bookmark(
    request_bookmark: BookmarkRequestModel,
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    bookmark = BookmarkModel(
        user_id=current_user['id'],
        movie_id=request_bookmark.movie_id
    )

    doc = json.loads(bookmark.json(by_alias=True))
    result = await mongo.load_one('bookmarks', doc)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': result.inserted_id}
    )


@router.delete(
    '/{bookmark_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_bookmark(
    bookmark_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    search = {
        '_id': str(bookmark_id),
        'user_id': str(current_user['id'])
    }
    result = await mongo.delete_one('bookmarks', search)
    if not result.deleted_count:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
