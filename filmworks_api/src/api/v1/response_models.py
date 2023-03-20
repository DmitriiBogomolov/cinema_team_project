from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class UUIDModel(BaseModel):
    id: UUID = Field(alias='uuid')

    class Config:
        allow_population_by_field_name = True


class Film(UUIDModel):
    title: str
    imdb_rating: Optional[float]


class Genre(UUIDModel):
    name: str


class Person(UUIDModel):
    full_name: str


class NestedPerson(UUIDModel):
    name: str = Field(alias='full_name')


class FilmDetail(Film):
    description: Optional[str]
    genres: List[Genre] = Field(alias='genre')
    actors: List[NestedPerson]
    writers: List[NestedPerson]
    directors: List[NestedPerson]


class NestedFilm(UUIDModel):
    roles: List[str]


class PersonDetail(Person):
    films: List[NestedFilm]
