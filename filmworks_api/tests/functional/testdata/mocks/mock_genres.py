"""
Тестовый набор данных для жанров.
Модель данных в сервисе:

class UUIDModel(BaseModel):
    id: UUID

class Genre(UUIDModel):
    name: str
    description: str | None = None
"""

import orjson
from uuid import UUID

from src.models.common import UUIDModel


class ResponseGenreModel(UUIDModel):
    """
    Ожидается, что json жанра на выходе из api соответствует
    значению, возвращаемому методом .json(by_alias=True) экземпляра тестовой модели
    """
    name: str

    def get_json(self):
        return orjson.loads(self.json(by_alias=True))


GENRES_LIST = [
    dict(
        id=UUID('26ffbc3e-c539-11ed-afa1-0242ac120002'),
        name='Genre2',
        description='Test'
    ),
    dict(
        id=UUID('26ffc094-c539-11ed-afa1-0242ac120002'),
        name='Genre1',
    ),
    dict(
        id=UUID('26ffc30a-c539-11ed-afa1-0242ac120002'),
        name='genre1',
        description='Test'
    ),
    dict(
        id=UUID('6ecc9a13-9150-44c3-869b-f0cf0aad3644'),
        name='Жанр1',
        description='Test'
    ),
    dict(
        id=UUID('feb1b3d3-ea76-4f7c-9ead-37d48f1198d1'),
        name='жанр1',
    ),
]
