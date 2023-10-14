from uuid import UUID
from typing_extensions import Self
from abc import ABC

from pydantic import EmailStr
from pydantic import BaseModel as PydanticBase


USE_MOCKS = True


class _BaseExternal(PydanticBase, ABC):
    @classmethod
    def get_list(cls, id_list: list[UUID]) -> list[Self]:
        if USE_MOCKS:
            return cls._get_mock_list(id_list)
        return cls._prefetch_list(id_list)

    @staticmethod
    def _prefetch_list(id_list: list[UUID]) -> list[Self]:
        pass

    @staticmethod
    def _get_mock_list(id_list: list[UUID]) -> list[Self]:
        pass


class User(_BaseExternal):
    id: UUID
    email: EmailStr | None

    @staticmethod
    def _prefetch_list(id_list: list[UUID]) -> list[Self]:
        pass

    @staticmethod
    def _get_mock_list(id_list: list[UUID]) -> list[Self]:
        return [User(id=cid, email='hello@yandex.ru') for cid in id_list]
