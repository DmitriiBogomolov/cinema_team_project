from pydantic import BaseModel
from typing import List, Optional


class UUIDModel(BaseModel):
    uuid: str


class Film(UUIDModel):
    title: str
    imdb_rating: Optional[float]


class Genre(UUIDModel):
    name: str


class Person(UUIDModel):
    full_name: str


class FilmDetail(Film):
    description: Optional[str]
    genre: List[Genre]
    actors: List[Person]
    writers: List[Person]
    directors: List[Person]


class NestedFilm(UUIDModel):
    roles: List[str]


class PersonDetail(Person):
    films: List[NestedFilm]
