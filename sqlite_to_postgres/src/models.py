import uuid
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Protocol


class IsDataclass(Protocol):
    __dataclass_fields__: ClassVar[Dict]


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: str
    type: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    rating: float = field(default=0.0)
    created: str = 'NOW()'
    modified: str = 'NOW()'

    def __post_init__(self):

        match self.type:
            case 'movie':
                self.type = 'MV'
            case 'tv_show':
                self.type = 'TV'
            case _:
                self.type = 'MV'


@dataclass
class Genre:
    name: str
    description: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: str = 'NOW()'
    modified: str = 'NOW()'


@dataclass
class GenreFilmWork:
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: str = 'NOW()'


@dataclass
class Person:
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: str = 'NOW()'
    modified: str = 'NOW()'


@dataclass
class PersonFilmWork:
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: str = 'NOW()'

    def __post_init__(self):

        match self.role:
            case 'actor':
                self.role = 'AR'
            case 'writer':
                self.role = 'WR'
            case 'director':
                self.role = 'DR'
            case _:
                self.role = 'AR'
