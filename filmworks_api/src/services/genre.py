from functools import lru_cache
from typing import List, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.common import Genre

SIZE = 200

SORT_PARAMETER = 'name.raw'


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return None

        return genre

    async def get_list(self) -> Optional[List[Genre]]:
        genres_list = await self._get_genres_list_from_elastic()
        if not genres_list:
            return None

        return genres_list

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None

        return Genre(
            uuid=doc['_source']['id'],
            name=doc['_source']['name'],
            description=doc['_source']['description']
        )

    async def _get_genres_list_from_elastic(self) -> Optional[List[Genre]]:
        try:
            resp = await self.elastic.search(
                                    index='genres',
                                    size=SIZE,
                                    sort=SORT_PARAMETER
                                    )
        except NotFoundError:
            return None

        return [Genre(uuid=doc['_source']['id'],
                      name=doc['_source']['name'],
                      description=doc['_source']['description']) for doc in resp['hits']['hits']]


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
