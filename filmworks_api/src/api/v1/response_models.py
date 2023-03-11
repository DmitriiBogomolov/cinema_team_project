from pydantic import BaseModel
from typing import List


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: float


class Genre(BaseModel):
    uuid: str
    name: str


class Person(BaseModel):
    uuid: str
    full_name: str


class FilmDetail(Film):
    description: str
    genre: List[Genre]
    actors: List[Person]
    writers: List[Person]
    directors: List[Person]


class NestedFilm(BaseModel):
    uuid: str
    roles: List[str]


class PersonDetail(Person):
    films: List[NestedFilm]
