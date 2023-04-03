import abc
from http import HTTPStatus

from pydantic import ValidationError
from fastapi import HTTPException

from src.services.repository.common import AbstractRepository
from src.models.common import UUIDModel


class BaseService(abc.ABC):
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    async def get_by_id(self,
                        index_name: str,
                        id: str,
                        model: UUIDModel
                        ) -> UUIDModel | None:

        instance = await self.repository.get_by_id(index_name, id)
        if not instance:
            return None

        try:
            response = model(**instance)
        except ValidationError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Something went wrong'
            )
        return response

    async def get_list(self,
                       index_name: str,
                       params: dict,
                       model: UUIDModel
                       ) -> list[UUIDModel] | None:

        instances = await self.repository.get_list(index_name, params)

        if not instances:
            return None

        try:
            response = [model(**instance) for instance in instances]
        except ValidationError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Something went wrong'
            )

        return response
