from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class NestedFilm(BaseModel):
    uuid: UUID
    roles: List[str]


class Person(BaseModel):
    uuid: UUID
    full_name: str
    films: List[Optional[NestedFilm]]


list_ = [
    Person(
        uuid=UUID('26ffbc3e-c539-11ed-afa1-0242ac120002'),
        full_name='Person',
        films=[]
    ),
    Person(
        uuid=UUID('26ffc094-c539-11ed-afa1-0242ac120002'),
        full_name='Person',
        films=[]
    ),
    Person(
        uuid=UUID('26ffc30a-c539-11ed-afa1-0242ac120002'),
        full_name='Person',
        films=[]
    ),
]
