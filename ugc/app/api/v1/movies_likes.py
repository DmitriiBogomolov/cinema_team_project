import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response, HTTPException
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from app.request_models import LikeRequestModel
from app.models import LikeModel
from app.core.jwt import access_check
from app.db.mongo import get_mongo_client
from app.services.repository import MongoRepository, get_mongo_repository


router = APIRouter()


@router.get('', response_model=list[LikeModel])
async def get_movie_likes(
    movie_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> list[LikeModel | None]:
    await authorize.jwt_required()

    search = {'entity_id': str(movie_id)}
    docs = await mongo.find(
        'filmworks_likes', search, [('created_at', -1)]
    )
    return [LikeModel(**doc)
            for doc in docs]


@router.get('/count')
async def get_movie_likes_count(
    movie_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()

    search = {'entity_id': str(movie_id)}
    count = await mongo.get_count('filmworks_likes', search)

    if not count:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'count': count}
    )


@router.get('/average')
async def get_movie_likes_average(
    movie_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> list[LikeModel | None]:
    await authorize.jwt_required()

    search = {'entity_id': str(movie_id)}
    average = await mongo.get_average(
        'filmworks_likes', search, 'rating'
    )

    if average == -1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'average': average}
    )


@router.post('')
async def post_movie_like(
    request_like: LikeRequestModel,
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    like = LikeModel(
        entity_id=request_like.entity_id,
        user_id=current_user['id'],
        rating=request_like.rating
    )

    doc = json.loads(like.json(by_alias=True))
    result = await mongo.load_one('filmworks_likes', doc)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': result.inserted_id}
    )


@router.patch('/{like_id}')
async def update_movie_like(
    like_id: UUID,
    request_like: LikeRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    mongo: MongoRepository = Depends(get_mongo_repository)
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
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    search = {
        '_id': str(like_id),
        'user_id': str(current_user['id'])
    }
    result = await mongo.delete_one('filmworks_likes', search)
    if not result.deleted_count:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
