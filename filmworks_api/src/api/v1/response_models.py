from pydantic import BaseModel, Field
from uuid import UUID


class UUIDModel(BaseModel):
    id: UUID = Field(alias='uuid')

    class Config:
        allow_population_by_field_name = True


class Film(UUIDModel):
    title: str
    imdb_rating: float | None = None


class Genre(UUIDModel):
    name: str


class Person(UUIDModel):
    full_name: str


class NestedPerson(UUIDModel):
    name: str = Field(alias='full_name')


class FilmDetail(Film):
    description: str | None = None
    genres: list[Genre] = Field(alias='genre')
    actors: list[NestedPerson]
    writers: list[NestedPerson]
    directors: list[NestedPerson]


class NestedFilm(UUIDModel):
    roles: list[str]


class PersonDetail(Person):
    films: list[NestedFilm | None]
