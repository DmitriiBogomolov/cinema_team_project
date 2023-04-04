from functools import lru_cache

from fastapi import Depends

from src.models.genre import Genre
from src.services.repository.elastic_repository import get_elastic_repository
from src.services.repository.common import AbstractRepository
from src.services.base_service import BaseService

SORT_PARAMETER = 'name.raw'


class GenreService(BaseService):
    @property
    def model(self):
        return Genre

    @property
    def index_name(self):
        return 'genres'

    async def get_list(self) -> list[Genre] | None:
        params = {
            'sort': SORT_PARAMETER
        }
        return await super().get_list(params)


@lru_cache()
def get_genre_service(
        repository: AbstractRepository = Depends(get_elastic_repository)
) -> GenreService:
    return GenreService(repository)
