from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.elastic import get_elastic
from src.services.repository.common import AbstractRepository
from src.services.repository.elastic_resolvers import (BasicParamsResolver,
                                                       MovieParamsResolver,
                                                       PersonParamsResolver)


class ElasticRepository(AbstractRepository):
    """Handle elasticsearch queries"""

    param_resolvers = {
        'movies': MovieParamsResolver,
        'persons': PersonParamsResolver,
        'genres': BasicParamsResolver
    }

    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index_name: str, id: str) -> dict | None:
        try:
            doc = await self.elastic.get(index=index_name, id=id)
        except NotFoundError:
            return None
        return doc['_source']

    async def get_list(self, index_name: str, params: dict) -> list[dict] | None:
        try:
            resolver = self.param_resolvers[index_name](params)

            resp = await self.elastic.search(
                index=index_name,
                **resolver.get_elastic_params()
            )

        except NotFoundError:
            return None
        docs = resp['hits']['hits']
        return [doc['_source'] for doc in docs]


@lru_cache()
def get_elastic_repository(
        elastic: ElasticRepository = Depends(get_elastic),
) -> ElasticRepository:
    return ElasticRepository(elastic)
