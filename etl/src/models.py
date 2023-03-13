"""
Application models for the
    - Nested
    - Filmwork
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class FilmworkNested(BaseModel):
    """Represents the nested objects from "movies" elasticsearch schema"""
    id: UUID
    name: str


class Filmwork(BaseModel):
    """Represents the objects from "movies" elasticsearch schema"""
    id: UUID
    imdb_rating: Optional[float] = None
    genre: List[str]
    title: str
    description: Optional[str] = None
    directors_names: List[str]
    actors_names: List[str]
    writers_names: List[str]
    directors: List[FilmworkNested]
    actors: List[FilmworkNested]
    writers: List[FilmworkNested]


class Genre(BaseModel):
    """Represents the objects from "genres" elasticsearch schema"""
    id: UUID
    name: str
    description: Optional[str] = None


class PersonNested(BaseModel):
    """Represents the nested objects from "person" elasticsearch schema"""
    id: UUID
    roles: List[str]


class Person(BaseModel):
    """Represents the objects from "genres" elasticsearch schema"""
    id: UUID
    full_name: str
    films: List[PersonNested]
