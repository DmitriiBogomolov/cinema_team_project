from models.common import UUIDModel
from models.nested import NestedPersonFilmwork


class Person(UUIDModel):
    """Represents a `person` object in schema."""
    full_name: str
    films: list[NestedPersonFilmwork]
