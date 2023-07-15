import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, status, Response
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError

from src.request_models import ReviewRequestModel, LikeRequestModel
from src.models import ReviewModel, LikeModel
from src.core.jwt import access_check
from src.db.mongo import get_mongo_client


router = APIRouter()


@router.get('', response_model=list[ReviewModel])
async def get_movie_reviews(
    movie_id: UUID,
    sort: str = 'empty',
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> list[ReviewModel | None]:
    await authorize.jwt_required()

    collection = mongo_client['ugc_db']['reviews']
    reviews_raw = await (
        collection.find({'movie_id': str(movie_id)})
                  .sort(sort, -1)
    ).to_list(length=None)

    if not reviews_raw:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )

    return [ReviewModel(**review_raw)
            for review_raw in reviews_raw]


@router.post('')
async def post_movie_review(
    reuqest_review: ReviewRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    collection = mongo_client['ugc_db']['reviews']
    review = ReviewModel(
        movie_id=reuqest_review.movie_id,
        author_id=current_user['id'],
        text=reuqest_review.text
    )

    try:
        result = await collection.insert_one(
            json.loads(review.json(by_alias=True))
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


@router.get('/<review_id>/likes', response_model=list[LikeModel])
async def get_review_likes(
    review_id: UUID,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> list[LikeModel | None]:
    await authorize.jwt_required()

    collection = mongo_client['ugc_db']['review_likes']
    movie_likes_raw = await (
        collection.find({'entity_id': str(review_id)})
                  .sort('created_at', -1)
    ).to_list(length=None)

    return [LikeModel(**movie_like_raw)
            for movie_like_raw in movie_likes_raw]


@router.post('/likes')
async def post_review_like(
    request_like: LikeRequestModel,
    authorize: AuthJWT = Depends(),
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
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

        inserted_like = await reviews_likes.insert_one(
            json.loads(like.json(by_alias=True))
        )
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
                    'likes_ids': str(inserted_like.inserted_id)
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
) -> JSONResponse:
    await authorize.jwt_required()
    current_user = access_check(await authorize.get_jwt_subject())

    reviews_likes = mongo_client['ugc_db']['reviews_likes']
    reviews = mongo_client['ugc_db']['reviews']

    like = await reviews_likes.find_one({
        '_id': str(like_id),
        'user_id': str(current_user['id'])
    })

    if not like:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={'message': 'not found'}
        )

    await reviews_likes.delete_one({
        '_id': str(like_id),
        'user_id': str(current_user['id'])
    })

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

    return None
