"""
Предоставляет репозиторий для обработки
лайков (оценок) рецензий
"""


from functools import lru_cache
from abc import abstractmethod

from fastapi import Depends

from app.models import LikeModel
from app.db.mongo import (
    AsyncIOMotorClient, get_mongo_client
)
from app.repositories.base import (
    BaseRepository
)
from app.repositories.reviews import (
    ReviewsRepository, get_reviews_repository
)
from app.repositories.zcommon import (
    OperationResult
)


class AbstractReviewsLikesRepository(BaseRepository):
    @abstractmethod
    async def get_list(
        self, review_id: str
    ) -> list[LikeModel]:
        pass

    @abstractmethod
    async def add(
        self, review_id: str, like: LikeModel
    ) -> OperationResult:
        pass

    @abstractmethod
    async def delete_for_user(
        self, review_id: str, user_id
    ) -> OperationResult:
        pass


class ReviewsLikesRepository(AbstractReviewsLikesRepository):
    """Репозиторий для обработки лайков (оценок) рецензий"""
    default_collection_name = 'reviews_likes'
    model_class = LikeModel

    def __init__(
        self,
        reviews_repository: ReviewsRepository,
        *args, **kwargs
    ):
        """
        Дополнительно к базовым зависимостям
        подключаем репозиторий самих рецензий
        """
        self.reviews_repository = reviews_repository
        BaseRepository.__init__(self, *args, **kwargs)

    async def get_list(
        self, review_id: str
    ) -> list[LikeModel]:
        """Получить список оценок рецензии"""
        return await \
            BaseRepository.search(
                self, {'entity_id': str(review_id)}
            )

    async def add(
        self, like: LikeModel
    ) -> OperationResult:
        """Получить количество оценок рецензии"""
        review = await \
            self.reviews_repository.get_by_id(
                like.entity_id
            )
        if not review:
            return None

        result = await BaseRepository.add(self, like)

        review.likes.append(like)
        await self.reviews_repository.replace(
            {'_id': str(review)}, like
        )

        return result

    async def delete_for_user(
        self, review_id: str, user_id
    ) -> OperationResult:
        """Получить рецензию, если та пренадлежит пользователю"""
        review = await \
            self.reviews_repository.get_by_id(
                str(review_id)
            )
        if not review:
            return None

        result = await BaseRepository.delete(
            self,
            {
                'entity_id': str(review_id),
                'user_id': str(user_id)
            }
        )
        if not result:
            return None

        review.likes = list(filter(
            lambda x: x['user_id'] != str(user_id),
            review.likes
        ))
        await self.reviews_repository.replace(
            review_id, review
        )

        return result


@lru_cache()
def get_reviews_likes_repository(
        reviews_repository: ReviewsRepository = (
            Depends(get_reviews_repository)
        ),
        mongo: AsyncIOMotorClient = (
            Depends(get_mongo_client)
        )
) -> ReviewsLikesRepository:
    return ReviewsLikesRepository(reviews_repository, mongo)
