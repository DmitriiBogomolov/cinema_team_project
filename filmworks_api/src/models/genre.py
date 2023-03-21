from models.common import UUIDModel


class Genre(UUIDModel):
    """Represents a `genre` object in schema."""
    name: str
    description: str | None = None
