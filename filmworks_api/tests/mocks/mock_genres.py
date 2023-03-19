from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Genre(BaseModel):
    uuid: UUID
    name: str
    description: Optional[str] = Field(None)


list_ = [
    Genre(
        uuid=UUID('26ffbc3e-c539-11ed-afa1-0242ac120002'),
        name='Genre 1',
        description='Test'
    ),
    Genre(
        uuid=UUID('26ffc094-c539-11ed-afa1-0242ac120002'),
        name='Genre 2'
    ),
    Genre(
        uuid=UUID('26ffc30a-c539-11ed-afa1-0242ac120002'),
        name='Genre 3',
        description='Test'
    ),
]
