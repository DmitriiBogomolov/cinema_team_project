from models.common import UUIDModel
from typing import Optional


class Genre(UUIDModel):
    """Represents a `genre` object in schema."""
    name: str
    description: Optional[str]
