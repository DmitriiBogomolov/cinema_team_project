"""
Предоставляет репозиторий для обработки закладок
(сохраненных фильмов пользователя)
"""

from functools import lru_cache
from abc import ABC, abstractmethod

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongo import get_mongo_client
from app.models import BasicModel, BookmarkModel
from app.repositories.base import (
    BaseRepository
)
from app.repositories.zcommon import (
    OperationResult,
)


class AbstractBookmarkRepository(ABC, BaseRepository):
    @abstractmethod
    async def get_list_for_user(
        self, user_id: str
    ) -> list[BookmarkModel]:
        pass

    @abstractmethod
    async def add(
        self, model: BasicModel
    ) -> OperationResult:
        pass

    @abstractmethod
    async def delete_for_user(
        self, bookmark_id: str, user_id: str
    ):
        pass


class BookmarkRepository(AbstractBookmarkRepository):
    """
    Репозиторий для обработки закладок
    (сохраненных фильмов пользователя)
    """
    default_collection_name = 'bookmarks'
    model_class = BookmarkModel

    async def get_list_for_user(
        self,
        user_id: str
    ) -> list[BookmarkModel]:
        """Получить закладки пользователя"""
        return await BaseRepository.search(
            self, {'user_id': str(user_id)}
        )

    async def add(
        self,
        bookmark: BookmarkModel
    ) -> OperationResult:
        """Получить закладку"""
        return await BaseRepository.add(
            self, bookmark
        )

    async def delete_for_user(
        self,
        bookmark_id: str,
        user_id: str
    ):
        """Удалить закладку, если та пренадлежит пользователю"""
        return await BaseRepository.delete(
            self,
            {'bookmark_id': bookmark_id, 'user_id': user_id}
        )


@lru_cache()
def get_bookmark_repository(
        mongo: AsyncIOMotorClient = Depends(get_mongo_client),
) -> AsyncIOMotorClient:
    return BookmarkRepository(mongo)
