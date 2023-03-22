from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from src.db.elastic import get_elastic
from src.db.redis import get_redis
from src.models.person import Person
from src.api.v1.common import PaginationParams

SORT_PARAMETER = 'full_name.raw'

INDEX_NAME = 'persons'


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._get_person_from_elastic(person_id)
        if not person:
            return None
        return person

    async def get_list(
            self,
            query: str = '',
            pp: PaginationParams | None = None,
            pit: str = ''
            ) -> list[Person] | None:

        persons_list = False
        params = {
            'query': query,
            'pp': pp,
            'pit': pit
        }

        persons_list = await self._get_persons_list_from_elastic(**params)
        if not persons_list:
            return None

        return persons_list

    async def _get_person_from_elastic(self, person_id: str) -> Person | None:
        try:
            doc = await self.elastic.get(INDEX_NAME, person_id)
        except NotFoundError:
            return None

        return Person(**doc['_source'])

    async def _get_persons_list_from_elastic(
            self,
            query: str = '',
            pp: PaginationParams | None = None,
            pit: str = ''
            ) -> list[Person] | None:

        try:
            offset = (pp.page_number-1) * pp.page_size
            query = {'match': {'full_name': query}} if query else None

            resp = await self.elastic.search(
                    query=query,
                    from_=offset,
                    size=pp.page_size,
                    sort=SORT_PARAMETER,
                    pit={'id': pit}
            )

        except NotFoundError:
            return None

        docs = resp['hits']['hits']

        return [Person(**doc['_source']) for doc in docs]


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
