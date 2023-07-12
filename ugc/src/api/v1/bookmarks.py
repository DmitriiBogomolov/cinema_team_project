from http import HTTPStatus

from fastapi import APIRouter, Depends
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.models import BookmarkModel
from src.core.jwt import access_check
from src.db.mongo import get_mongo_client


router = APIRouter()


@router.get('')
async def get_bookmark(
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(
        await authorize.get_jwt_subject()
    )

    try:
        await mongo_client.admin.command('ping')
        current_user
        print('Pinged your deployment. You successfully connected to MongoDB!')
    except Exception as e:
        print(e)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'}
    )


@router.post('')
async def load_bookmark(
    bookmark: BookmarkModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(
        await authorize.get_jwt_subject()
    )

    collection = mongo_client['ugc_db']['bookmarks']

    if await collection.count_documents({
        'user_id': str(current_user['id']),
        'movie_id': str(bookmark.movie_id)
    }):
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': 'already exists'}
        )

    result = await collection.insert_one({
        'user_id': str(current_user['id']),
        'movie_id': str(bookmark.movie_id)
    })

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': str(result.inserted_id)}
    )
