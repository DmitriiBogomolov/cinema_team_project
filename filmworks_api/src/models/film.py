from typing import List, Optional

from models.common import UUIDModel
from models.nested import NestedGenre, NestedPerson


class Filmwork(UUIDModel):
    """Represents a `filmwork` object in schema."""
    title: str
    imdb_rating: Optional[float] = None
    description: Optional[str] = None
    genres: List[NestedGenre]
    actors: List[NestedPerson]
    directors: List[NestedPerson]
    writers: List[NestedPerson]
