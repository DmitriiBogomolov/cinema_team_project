"""
Предоставляет репозиторий для обработки
лайков (оценок) фильмов
"""

from functools import lru_cache
from abc import ABC, abstractmethod

from fastapi import Depends
from motor.motor_asyncio import (
    AsyncIOMotorClient
)

from app.db.mongo import get_mongo_client
from app.models import LikeModel
from app.repositories.base import (
    BaseRepository
)
from app.repositories.zcommon import (
    OperationResult
)


class AbstractMoviesLikesRepository(ABC, BaseRepository):
    @abstractmethod
    async def get_list(
        self, movie_id: str
    ) -> list[LikeModel]:
        pass

    @abstractmethod
    async def get_count(
        self, movie_id: str
    ) -> int:
        pass

    @abstractmethod
    async def get_average_rating(
        self, movie_id: str
    ) -> int:
        pass

    @abstractmethod
    async def add(
        self, like: LikeModel
    ) -> OperationResult:
        pass

    @abstractmethod
    async def delete_for_user(
        self, movie_id: str
    ):
        pass


class MoviesLikesRepository(AbstractMoviesLikesRepository):
    """Репозиторий для обработки лайков (оценок) фильмов"""
    default_collection_name = 'filmworks_likes'
    model_class = LikeModel

    async def get_list(
        self, movie_id: str
    ) -> list[LikeModel]:
        """Получить список оценок фильма"""
        return await (
            BaseRepository.search(
                self, {'entity_id': str(movie_id)}
            )
        )

    async def get_count(
        self, movie_id: str
    ) -> int:
        """Получить количество оценок фильма"""
        return await BaseRepository.count(
            self, {'entity_id': str(movie_id)}
        )

    async def get_average_rating(self, movie_id: str) -> int:
        """Получить среднюю оценку фильма"""
        return await BaseRepository.average(
            self,
            {'entity_id': str(movie_id)},
            'rating'
        )

    async def add(self, like: LikeModel) -> OperationResult:
        """Добавить оценку"""
        return await BaseRepository.add(self, like)

    async def delete_for_user(self, movie_id: str, user_id: str):
        """Удалить оценку, если та пренадлежит пользователю"""
        return await BaseRepository.delete(
            self,
            {'entity_id': str(movie_id), 'user_id': str(user_id)}
        )


@lru_cache()
def get_movies_likes_repository(
        mongo: AsyncIOMotorClient = Depends(get_mongo_client)
) -> MoviesLikesRepository:
    return MoviesLikesRepository(mongo)
