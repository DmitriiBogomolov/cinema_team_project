"""
Репозиторий для хранения данных о событиях
"""

from functools import lru_cache
from abc import ABC, abstractmethod

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.models import _BasicSingleEvent, _BasicMultipleEvent
from app.db.mongo import get_mongo_client


class AbstractRepository(ABC):
    @abstractmethod
    async def save_single(self, event: _BasicSingleEvent):
        pass

    @abstractmethod
    async def save_multiple(self, multiple: _BasicMultipleEvent):
        pass

    async def search(self, search: dict) -> list:
        pass


class MongoRepository(AbstractRepository):
    """
    Репозиторий для хранения данных о событиях в mongodb
    """
    db_name = 'notification'
    collection_name = 'events'

    def __init__(self, mongo: AsyncIOMotorClient):
        self.mongo = mongo

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Возвращает объект коллекции"""

        return (
            self.mongo[self.db_name]
                      [self.collection_name]
        )

    async def save_single(self, event: _BasicSingleEvent):
        await self.collection.insert_one(event.to_mongo())

    async def save_multiple(self, event: _BasicMultipleEvent):
        await self.collection.insert_many(event.to_mongo())

    async def search(self, search: dict, model_class) -> list:
        docs = await (
            self.collection
                .find(search)
                .sort([('created_at', -1)])
        ).to_list(length=None)

        return [model_class(**doc)
                for doc in docs]

    async def count(self, search: dict) -> int:
        """Количество документов по условию поиска"""

        return await (
            self.collection.count_documents(search)
        )


@lru_cache()
def get_repository(
        mongo: AsyncIOMotorClient = Depends(get_mongo_client),
) -> AbstractRepository:
    return MongoRepository(mongo)
