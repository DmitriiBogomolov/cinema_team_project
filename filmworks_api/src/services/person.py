from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from src.api.v1.common import PaginationParams
from src.db.redis import get_redis
from src.models.person import Person
from src.services.elastic_manager.elastic_handler import (ElasticHandler,
                                                          get_elastic_handler)
from src.services.elastic_manager.search_models import PersonSearch

SORT_PARAMETER = 'full_name.raw'

INDEX_NAME = 'persons'


class PersonService:
    def __init__(self, redis: Redis, elastic_handler: ElasticHandler):
        self.redis = redis
        self.elastic_handler = elastic_handler

    async def get_by_id(self, person_id: str) -> Person | None:
        doc = await self.elastic_handler.get_by_id(INDEX_NAME, person_id)
        if not doc:
            return None
        return Person(**doc['_source'])

    async def get_list(
            self,
            query: str | None = None,
            pp: PaginationParams | None = None
            ) -> list[Person] | None:

        search = PersonSearch(
            sort=SORT_PARAMETER,
            pp=pp
        )
        search.add_match_query(query)

        docs = await self.elastic_handler.search(search)
        persons_list = [Person(**doc['_source']) for doc in docs]

        if not persons_list:
            return None

        return persons_list


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic_handler: ElasticHandler = Depends(get_elastic_handler)
) -> PersonService:
    return PersonService(redis, elastic_handler)
