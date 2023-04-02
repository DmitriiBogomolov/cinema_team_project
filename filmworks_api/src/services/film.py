from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from src.api.v1.common import PaginationParams
from src.db.redis import get_redis
from src.models.film import Filmwork
from src.services.elastic_manager.elastic_handler import (ElasticHandler,
                                                          get_elastic_handler)
from src.services.elastic_manager.search_models import FilmSearch


class FilmService:
    def __init__(self, redis: Redis, elastic_handler: ElasticHandler):
        self.redis = redis
        self.elastic_handler = elastic_handler

    async def get_by_id(self, film_id: str) -> Filmwork | None:
        doc = await self.elastic_handler.get_by_id('movies', film_id)
        if not doc:
            return None

        return Filmwork(**doc['_source'])

    async def get_search(
            self,
            query: str | None = None,
            genre: str | None = None,
            pp: PaginationParams | None = None,
            by_ids: list[str] | None = None,
            sort: str | None = None
            ) -> list[Filmwork] | None:

        search = FilmSearch(
            sort=sort,
            pp=pp
        )

        search.add_multi_match_query(query)
        search.add_nested_genre_query(genre)
        search.add_by_ids_query(by_ids)
        docs = await self.elastic_handler.search(search)

        films = [Filmwork(**doc['_source']) for doc in docs]

        if not films:
            return None
        return films


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic_handler: ElasticHandler = Depends(get_elastic_handler)
) -> FilmService:
    return FilmService(redis, elastic_handler)
