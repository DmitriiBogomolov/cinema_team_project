from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from src.db.redis import get_redis
from src.models.genre import Genre
from src.services.elastic_manager.elastic_handler import (ElasticHandler,
                                                          get_elastic_handler)
from src.services.elastic_manager.search_models import GenreSearch

SORT_PARAMETER = 'name.raw'


class GenreService:
    def __init__(self, redis: Redis, elastic_handler: ElasticHandler):
        self.redis = redis
        self.elastic_handler = elastic_handler

    async def get_by_id(self, genre_id: str) -> Genre | None:
        doc = await self.elastic_handler.get_by_id('genres', genre_id)

        if not doc:
            return None

        return Genre(**doc['_source'])

    async def get_list(self) -> list[Genre] | None:

        search = GenreSearch(
            sort=SORT_PARAMETER
        )

        docs = await self.elastic_handler.search(search)
        genres_list = [Genre(**doc['_source']) for doc in docs]

        if not genres_list:
            return None

        return genres_list


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic_handler: ElasticHandler = Depends(get_elastic_handler)
) -> GenreService:
    return GenreService(redis, elastic_handler)
