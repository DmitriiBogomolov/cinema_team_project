from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import DeleteResult, InsertOneResult

from app.db.mongo import get_mongo_client


import abc


class AbstractRepository(abc.ABC):
    pass
    '''
    @abc.abstractmethod
    def get_by_id(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_list(self, *args, **kwargs):
        pass
    '''


class MongoRepository(AbstractRepository):
    """Handle MongoDB queries"""
    db_name = 'ugc_db'

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client

    async def find(
        self,
        collection: str,
        search: dict = {},
        sort: list[tuple[str, int]] | None = None
    ) -> list[dict] | None:
        collection = self.mongo_client[self.db_name][collection]
        if sort:
            return await (
                collection.find(search).sort(sort)
            ).to_list(length=None)
        else:
            return await (
                collection.find(search)
            ).to_list(length=None)

    async def find_one(
        self,
        collection: str,
        search: dict = {}
    ) -> list[dict] | None:
        collection = self.mongo_client[self.db_name][collection]
        return await (collection.find_one(search))

    async def load_one(
        self,
        collection: str,
        doc: dict = {}
    ) -> InsertOneResult | None:
        collection = self.mongo_client[self.db_name][collection]
        return await collection.insert_one(doc)

    async def delete_one(
        self,
        collection: str,
        search: dict
    ) -> DeleteResult | None:
        collection = self.mongo_client[self.db_name][collection]
        return await collection.delete_one(search)

    async def get_count(
        self,
        collection: str,
        search: dict
    ) -> int | None:
        collection = self.mongo_client['ugc_db'][collection]
        return await (collection.count_documents(search))

    async def get_average(
        self,
        collection: str,
        search: dict,
        avg_field: str
    ) -> int:
        collection = self.mongo_client['ugc_db'][collection]
        result = await (
            collection.aggregate([
                {'$match': search},
                {
                    '$group': {
                        '_id': 'null',
                        'avg_val': {'$avg': f'${avg_field}'}
                    }
                }
            ])
        ).to_list(length=None)

        if not result:
            return -1
        return result[0]['avg_val']


@lru_cache()
def get_mongo_repository(
        mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
) -> MongoRepository:
    return MongoRepository(mongo_client)
