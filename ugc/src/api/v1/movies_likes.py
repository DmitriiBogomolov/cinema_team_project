import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from src.request_models import LikeRequestModel
from src.models import LikeModel
from src.core.jwt import access_check
from src.db.mongo import get_mongo_client


router = APIRouter()


@router.get('', response_model=list[LikeModel])
async def get_movie_likes(
    movie_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> list[LikeModel | None]:
    await authorize.jwt_required()

    collection = mongo_client['ugc_db']['filmworks_likes']
    movie_likes_raw = await (
        collection.find({'entity_id': str(movie_id)})
                  .sort('created_at', -1)
    ).to_list(length=None)

    return [LikeModel(**movie_like_raw)
            for movie_like_raw in movie_likes_raw]


@router.get('/count')
async def get_movie_likes_count(
    movie_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()

    collection = mongo_client['ugc_db']['filmworks_likes']
    movie_likes_count = await (
        collection.count_documents({'entity_id': str(movie_id)})
    )

    if not movie_likes_count:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'count': movie_likes_count}
    )


@router.get('/average')
async def get_movie_likes_average(
    movie_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> list[LikeModel | None]:
    await authorize.jwt_required()

    collection = mongo_client['ugc_db']['filmworks_likes']
    movie_likes_average = await (
        collection.aggregate([
            {'$match': {'entity_id': {'$eq': str(movie_id)}}},
            {
                '$group': {
                    '_id': 'null',
                    'avg_val': {'$avg': '$rating'}
                }
            }
        ])
    ).to_list(length=None)

    if not movie_likes_average:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'average': movie_likes_average[0]['avg_val']}
    )


@router.post('')
async def post_movie_like(
    request_like: LikeRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['filmworks_likes']
    like = LikeModel(
        entity_id=request_like.entity_id,
        user_id=current_user['id'],
        rating=request_like.rating
    )

    try:
        result = await collection.insert_one(
            json.loads(like.json(by_alias=True))
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


@router.patch('/{like_id}')
async def update_movie_like(
    like_id: UUID,
    request_like: LikeRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['filmworks_likes']
    like = LikeModel(
        _id=like_id,
        entity_id=request_like.entity_id,
        user_id=current_user['id'],
        rating=request_like.rating
    )

    result = await collection.replace_one(
        {'_id': str(like_id), 'user_id': str(current_user['id'])},
        json.loads(like.json(by_alias=True))
    )

    if not result.modified_count:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'updated': 'ok'}
    )


@router.delete(
    '/{like_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_movie_like(
    like_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['filmworks_likes']

    result = await collection.delete_one({
        '_id': str(like_id),
        'user_id': str(current_user['id'])
    })

    if not result.deleted_count:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )
    return None
