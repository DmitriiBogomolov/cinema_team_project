"""
Предоставляет репозиторий для обработки
рецензий к фильму
"""

from functools import lru_cache
from abc import ABC, abstractmethod

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongo import get_mongo_client
from app.models import ReviewModel
from app.repositories.base import BaseRepository
from app.repositories.zcommon import SortParam
from app.repositories.zcommon import (
    OperationResult
)


class AbstractReviewsRepository(ABC, BaseRepository):
    @abstractmethod
    async def get_by_id(
        self,
        review_id: str
    ) -> ReviewModel | None:
        pass

    @abstractmethod
    async def get_list_for_movie(
        self,
        movie_id: str,
        sort: SortParam | None
    ) -> list[ReviewModel]:
        pass

    @abstractmethod
    async def add(
        self,
        review: ReviewModel
    ) -> OperationResult:
        pass

    @abstractmethod
    async def replace(
        self,
        review_id: str,
        review: ReviewModel
    ) -> OperationResult:
        pass

    @abstractmethod
    async def delete_for_user(
        self,
        review_id: str,
        user_id: str
    ):
        pass


class ReviewsRepository(AbstractReviewsRepository):
    """Репозиторий для обработки рецензий к фильму"""
    default_collection_name = 'reviews'
    model_class = ReviewModel

    async def get_by_id(
        self,
        review_id: str
    ) -> ReviewModel | None:
        """Получить рецензию по ID"""
        return await \
            BaseRepository.get_by_id(self, review_id)

    async def get_list_for_movie(
        self,
        movie_id: str,
        sort: SortParam | None
    ) -> list[ReviewModel]:
        """Получить список рецензий фильма"""
        return await \
            BaseRepository.search(
                self, {'movie_id': str(movie_id)}, sort
            )

    async def add(
        self,
        review: ReviewModel
    ) -> OperationResult:
        """Добавить рецензию"""
        return await BaseRepository.add(self, review)

    async def replace(
        self,
        review_id: str,
        review: ReviewModel
    ) -> OperationResult:
        """Заменить (обновить) документ рецензии рецензии"""
        return await \
            BaseRepository.replace(
                self, {'_id': str(review_id)}, review
            )

    async def delete_for_user(
        self,
        review_id: str,
        user_id: str
    ):
        """Удалить рецензию, если она принадлежит пользователю"""
        return await \
            BaseRepository.delete(
                self,
                {'_id': str(review_id), 'user_id': str(user_id)}
            )


@lru_cache()
def get_reviews_repository(
        mongo: AsyncIOMotorClient = Depends(get_mongo_client),
) -> ReviewsRepository:
    return ReviewsRepository(mongo)
