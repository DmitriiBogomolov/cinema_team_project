from models.common import UUIDModel


class NestedGenre(UUIDModel):
    """Represents a nested `genre` object in schema."""
    name: str


class NestedPerson(UUIDModel):
    """Represents a nested `person` object in schema."""
    name: str


class NestedPersonFilmwork(UUIDModel):
    """Represents a nested `person_filmwork` relation."""
    roles: list[str]
