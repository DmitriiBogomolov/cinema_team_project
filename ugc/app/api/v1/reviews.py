import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response, HTTPException
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from app.request_models import ReviewRequestModel, LikeRequestModel
from app.models import ReviewModel, LikeModel
from app.core.jwt import access_check
from app.db.mongo import get_mongo_client
from app.services.common import SortParam
from app.services.repository import MongoRepository, get_mongo_repository


router = APIRouter()


@router.get('', response_model=list[ReviewModel])
async def get_movie_reviews(
    movie_id: UUID,
    sort: SortParam = Depends(),
    authorize: AuthJWT = Depends(),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> list[ReviewModel | None]:
    await authorize.jwt_required()

    search = {'movie_id': str(movie_id)}
    docs = await mongo.find(
        'reviews', search, sort.list or [('rating', -1)]
    )

    if not docs:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )

    return [ReviewModel(**doc)
            for doc in docs]


@router.post('')
async def post_movie_review(
    reuqest_review: ReviewRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    review = ReviewModel(
        movie_id=reuqest_review.movie_id,
        author_id=current_user['id'],
        text=reuqest_review.text
    )

    doc = json.loads(review.json(by_alias=True))
    result = await mongo.load_one('reviews', doc)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': result.inserted_id}
    )


@router.get('/{review_id}/likes', response_model=list[LikeModel])
async def get_review_likes(
    review_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> list[LikeModel | None]:
    await authorize.jwt_required()

    search = {'entity_id': str(review_id)}
    docs = await mongo.find(
        'reviews_likes', search, [('created_at', -1)]
    )

    return [LikeModel(**doc)
            for doc in docs]


@router.post('/likes')
async def post_review_like(
    request_like: LikeRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    like = LikeModel(
        entity_id=request_like.entity_id,
        user_id=current_user['id'],
        rating=request_like.rating
    )

    try:
        reviews_likes = mongo_client['ugc_db']['reviews_likes']
        reviews = mongo_client['ugc_db']['reviews']

        if not reviews.count_documents(
            {'_id': request_like.entity_id}
        ):
            return JSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={'message': 'not found'}
            )

        like_doc = json.loads(like.json(by_alias=True))
        inserted_like = await mongo.load_one('reviews_likes', like_doc)

        new_rating_raw = await (
            reviews_likes.aggregate([
                {'$match': {'entity_id': {'$eq': str(like.entity_id)}}},
                {
                    '$group': {
                        '_id': 'null',
                        'avg_val': {'$avg': '$rating'}
                    }
                }
            ])
        ).to_list(length=None)
        new_rating = new_rating_raw[0]['avg_val']

        await reviews.update_one(
            {'_id': str(request_like.entity_id)},
            {
                '$set': {'rating': new_rating},
                '$push': {
                    'likes_ids': inserted_like.inserted_id
                }
            }
        )
    except DuplicateKeyError:
        return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={'message': 'already exists'}
        )

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        content={'inserted': str(inserted_like.inserted_id)}
    )


@router.delete(
    '/likes/{like_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response
)
async def delete_review_like(
    like_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    mongo: MongoRepository = Depends(get_mongo_repository)
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    reviews_likes = mongo_client['ugc_db']['reviews_likes']
    reviews = mongo_client['ugc_db']['reviews']

    search = {
        '_id': str(like_id),
        'user_id': str(current_user['id'])
    }
    like = await mongo.find_one('reviews_likes', search)

    if not like:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete_one('reviews_likes', like)

    new_rating_raw = await (
        reviews_likes.aggregate([
            {'$match': {'entity_id': {'$eq': str(like['entity_id'])}}},
            {
                '$group': {
                    '_id': 'null',
                    'avg_val': {'$avg': '$rating'}
                }
            }
        ])
    ).to_list(length=None)
    if new_rating_raw:
        new_rating = new_rating_raw[0]['avg_val']
    else:
        new_rating = 0

    await reviews.update_one(
        {'_id': str(like['entity_id'])},
        {
            '$set': {'rating': new_rating},
            '$pull': {
                'likes_ids': str(like['_id'])
            }
        }
    )
