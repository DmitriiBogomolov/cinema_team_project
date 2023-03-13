"""
Application models for the
    - Nested
    - Filmwork
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Nested(BaseModel):
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
    directors: List[Nested]
    actors: List[Nested]
    writers: List[Nested]


class Genre(BaseModel):
    """Represents the objects from "genres" elasticsearch schema"""
    id: UUID
    name: str
    description: Optional[str] = None


class Person(BaseModel):
    """Represents the objects from "genres" elasticsearch schema"""
    id: UUID
    full_name: str
