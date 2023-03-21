from src.models.common import UUIDModel
from src.models.nested import NestedGenre, NestedPerson


class Filmwork(UUIDModel):
    """Represents a `filmwork` object in schema."""
    title: str
    imdb_rating: float | None = None
    description: str | None = None
    genres: list[NestedGenre]
    actors: list[NestedPerson]
    directors: list[NestedPerson]
    writers: list[NestedPerson]
