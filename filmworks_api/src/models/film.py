import orjson
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class UUIDModel(BaseModel):
    """Core schema object."""
    uuid: UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class NestedGenre(UUIDModel):
    """Represents a nested `genre` object in schema."""
    name: str


class NestedPerson(UUIDModel):
    """Represents a nested `person` object in schema."""
    full_name: str


class Filmwork(UUIDModel):
    """Represents a `filmwork` object in schema."""
    title: str
    imdb_rating: Optional[float] = None
    description: Optional[str] = None
    genre: List[NestedGenre]
    actors: List[NestedPerson]
    director: List[NestedPerson]
    writers: List[NestedPerson]


class Genre(UUIDModel):
    """Represents a `genre` object in schema."""
    name: str
    description: str


class Person(UUIDModel):
    """Represents a `person` object in schema."""
    full_name: str
    role: str
    film_ids: List[UUID] = []
