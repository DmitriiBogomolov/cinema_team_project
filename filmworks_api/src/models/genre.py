from typing import Optional

from src.models.common import UUIDModel


class Genre(UUIDModel):
    """Represents a `genre` object in schema."""
    name: str
    description: Optional[str]
