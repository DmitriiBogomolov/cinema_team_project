from functools import lru_cache

from fastapi import Depends

from src.api.v1.common import PaginationParams
from src.models.film import Filmwork
from src.services.repository.elastic_repository import get_elastic_repository
from src.services.repository.common import AbstractRepository
from src.services.base_service import BaseService


class FilmService(BaseService):
    async def get_by_id(self, film_id: str) -> Filmwork | None:
        return await super().get_by_id('movies', film_id, Filmwork)

    async def get_list(
            self,
            query: str | None = None,
            genre: str | None = None,
            pp: PaginationParams | None = None,
            by_ids: list[str] | None = None,
            sort: str | None = None
            ) -> list[Filmwork] | None:

        params = {
            'sort': sort,
            'pp': pp,
            'movie': query,
            'genres': genre,
            'by_ids': by_ids
        }

        return await super().get_list('movies', params, Filmwork)


@lru_cache()
def get_film_service(
        repository: AbstractRepository = Depends(get_elastic_repository)
) -> FilmService:
    return FilmService(repository)
