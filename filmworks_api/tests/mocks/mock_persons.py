from uuid import UUID

from pydantic import BaseModel


class NestedFilm(BaseModel):
    uuid: UUID
    roles: list[str]


class Person(BaseModel):
    uuid: UUID
    full_name: str
    films: list[NestedFilm] | None = None


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
