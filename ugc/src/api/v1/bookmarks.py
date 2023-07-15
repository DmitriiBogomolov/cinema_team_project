import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from src.request_models import BookmarkRequestModel
from src.models import BookmarkModel
from src.core.jwt import access_check
from src.db.mongo import get_mongo_client


router = APIRouter()


@router.get('', response_model=list[BookmarkModel])
async def get_bookmarks(
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> list[BookmarkModel | None]:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['bookmarks']
    bookmarks_raw = await (
        collection
        .find({'user_id': str(current_user['id'])})
        .sort('created_at', -1)
    ).to_list(length=None)

    return [BookmarkModel(**bookmark_raw)
            for bookmark_raw in bookmarks_raw]


@router.post('')
async def post_bookmark(
    request_bookmark: BookmarkRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['bookmarks']
    bookmark = BookmarkModel(
        user_id=current_user['id'],
        movie_id=request_bookmark.movie_id
    )

    try:
        result = await collection.insert_one(
            json.loads(bookmark.json(by_alias=True))
        )
    except DuplicateKeyError:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': 'already exists'}
        )

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': str(result.inserted_id)}
    )


@router.delete(
    '/{bookmark_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_bookmark(
    bookmark_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['bookmarks']

    result = await collection.delete_one({
        '_id': str(bookmark_id),
        'user_id': str(current_user['id'])
    })

    if not result.deleted_count:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )
    return None
