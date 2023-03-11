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
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[Nested]
    writers: List[Nested]


class Genre(BaseModel):
    """Represents the objects from "genres" elasticsearch schema"""
    id: UUID
    name: str
    description: Optional[str] = None
