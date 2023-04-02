from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from src.db.elastic import get_elastic
from src.services.elastic_manager import search_models


class ElasticHandler:
    """Handle elasticsearch queries"""
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, index_name: str, id: str) -> dict:
        """
        Get document by id from elastic.
            Parameters:
                index_name: Elastic index for search.
                id: Document ID.
            Returns:
                Document (dict) with specified id.
        """
        try:
            doc = await self.elastic.get(index_name, id)
        except NotFoundError:
            return None
        return doc

    async def search(self, search: search_models.Search) -> list[dict]:
        """
        Search documents in elastic.
            Parameters:
                search: Search model object, provides search parameters for elastic.
                        Must be inherited from search_models.Search.
            Returns:
                List of hits documents (dict).
        """
        try:
            resp = await self.elastic.search(**search.get_search_params())

        except NotFoundError:
            return None
        docs = resp['hits']['hits']
        return docs


@lru_cache()
def get_elastic_handler(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> ElasticHandler:
    return ElasticHandler(elastic)
