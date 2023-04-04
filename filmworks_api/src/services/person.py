from functools import lru_cache

from fastapi import Depends

from src.api.v1.common import PaginationParams
from src.models.person import Person
from src.services.repository.elastic_repository import get_elastic_repository
from src.services.repository.common import AbstractRepository
from src.services.base_service import BaseService

SORT_PARAMETER = 'full_name.raw'


class PersonService(BaseService):
    @property
    def model(self):
        return Person

    @property
    def index_name(self):
        return 'persons'

    async def get_list(
            self,
            query: str | None = None,
            pp: PaginationParams | None = None
    ) -> list[Person] | None:

        params = {
            'sort': SORT_PARAMETER,
            'pp': pp,
            'full_name': query
        }

        return await super().get_list(params)


@lru_cache()
def get_person_service(
        repository: AbstractRepository = Depends(get_elastic_repository)
) -> PersonService:
    return PersonService(repository)
