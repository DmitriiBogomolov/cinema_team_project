from abc import ABC, abstractmethod
from http import HTTPStatus

from pydantic import ValidationError
from fastapi import HTTPException
from fastapi_request_id import get_request_id

from src.services.repository.common import AbstractRepository
from src.models.common import UUIDModel
from src.core.logger import logger


class BaseService(ABC):
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    @property
    @abstractmethod
    def model(self):
        pass

    @property
    @abstractmethod
    def index_name(self):
        pass

    async def get_by_id(self, doc_id: str) -> UUIDModel | None:

        instance = await self.repository.get_by_id(self.index_name, doc_id)
        if not instance:
            return None

        try:
            response = self.model(**instance)
        except ValidationError as e:
            logger.warning(e, extra={'request_id': get_request_id()})
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Something went wrong'
            )
        return response

    async def get_list(self,
                       params: dict
                       ) -> list[UUIDModel] | None:

        instances = await self.repository.get_list(self.index_name, params)

        if not instances:
            return None

        try:
            response = [self.model(**instance) for instance in instances]
        except ValidationError as e:
            logger.warning(e, extra={'request_id': get_request_id()})
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Something went wrong'
            )

        return response
