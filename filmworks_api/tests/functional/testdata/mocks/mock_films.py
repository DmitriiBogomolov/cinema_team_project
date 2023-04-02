"""
Тестовый набор данных для фильмов.
"""

import orjson
from uuid import UUID
from pydantic import Field

from src.models.common import UUIDModel
from src.models.nested import NestedGenre


class NestedPerson(UUIDModel):
    name: str = Field(alias='full_name')


class ResponseFilmDetailModel(UUIDModel):
    title: str
    imdb_rating: float | None = None
    description: str | None = None
    genres: list[NestedGenre] = Field(alias='genre')
    actors: list[NestedPerson]
    writers: list[NestedPerson]
    directors: list[NestedPerson]

    def get_json(self):
        return orjson.loads(self.json(by_alias=True))


class ResponseFilmModel(UUIDModel):
    title: str
    imdb_rating: float | None = None

    def get_json(self):
        return orjson.loads(self.json(by_alias=True))


FILMS_LIST = [
    dict(
        id=UUID('025c58cd-1b7e-43be-9ffb-8571a613577b'),
        title='Film Detail',
        imdb_rating=8.0,
        description='Test Description',
        genres=[
            dict(
                id='120a21cf-9097-479e-904a-13dd7198c1dd',
                name='Adventure'
            ),
            dict(
              id='3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff',
              name='Action'
            ),
            dict(
              id='6c162475-c7ed-4461-9184-001ef3d9f26e',
              name='Sci-Fi'
            ),
            dict(
              id='b92ef010-5e4c-4fd0-99d6-41b6456272cd',
              name='Fantasy'
            )
        ],
        actors=[
            dict(
              id='26e83050-29ef-4163-a99d-b546cac208f8',
              name='Mark Hamill'
            ),
            dict(
              id='5b4bf1bc-3397-4e83-9b17-8b10c6544ed1',
              name='Harrison Ford'
            ),
            dict(
              id='b5d2b63a-ed1f-4e46-8320-cf52a32be358',
              name='Carrie Fisher'
            ),
            dict(
              id='efdd1787-8871-4aa9-b1d7-f68e55b913ed',
              name='Billy Dee Williams'
            )
        ],
        writers=[
            dict(
              id='3217bc91-bcfc-44eb-a609-82d228115c50',
              name='Lawrence Kasdan'
            ),
            dict(
              id='a5a8f573-3cee-4ccc-8a2b-91cb9f55250a',
              name='George Lucas'
            )
        ],
        directors=[
            dict(
              id='3214cf58-8dbf-40ab-9185-77213933507e',
              name='Richard Marquand'
            )
        ]
    ),
    dict(
        id=UUID('025c58cd-1b7e-43be-9ffb-8571a616877b'),
        title='Test Movie 1',
        imdb_rating=6.3,
        description='Test',
        genres=[
            dict(
                id='120a21cf-9097-479e-904a-13dd7198c1dd',
                name='Adventure'
            ),
            dict(
              id='b92ef010-5e4c-4fd0-99d6-41b6456272cd',
              name='Fantasy'
            )
        ],
        actors=[],
        writers=[],
        directors=[]
    ),
    dict(
        id=UUID('26ffc095-c539-11ed-afa1-0242ac120003'),
        title='Test Movie 2',
        imdb_rating=7.5,
        description='Test',
        directors_names=['Diane Cooper'],
        genres=[
            dict(
                id='120a21cf-9097-479e-904a-13dd7198c1dd',
                name='Adventure'
            ),
        ],
        actors=[],
        writers=[],
        directors=[
            dict(
              id='637a59c5-8bf8-4d2c-a092-d8c6440cd7ed',
              name='Diane Cooper'
            )
        ]
    ),
    dict(
        id=UUID('26ffc30a-c539-11ed-afa1-0242ac120002'),
        title='Тестовый Фильм 3',
        imdb_rating=4.1,
        description='Test',
        writers_names=['Ben Cooper'],
        genres=[
            dict(
                id='120a21cf-9097-479e-904a-13dd7198c1dd',
                name='Adventure'
            ),
        ],
        actors=[],
        writers=[
            dict(
              id='637a59c5-8bf8-4d2c-a092-d8c6440cd7ed',
              name='Ben Cooper'
            )
        ],
        directors=[]
    ),
    dict(
        id=UUID('6ecc9a13-9150-44c3-869b-f0cf0aad3644'),
        title='Тестовый Фильм 4',
        imdb_rating=5.8,
        genres=[
            dict(
                id='120a21cf-9097-479e-904a-13dd7198c1dd',
                name='Adventure'
            ),
        ],
        actors=[],
        writers=[],
        directors=[]
    ),
    dict(
        id=UUID('feb1b3d3-ea76-4f7c-9ead-37d48f1198d1'),
        title='Тестовый Фильм 4',
        imdb_rating=8.8,
        actors_names=['George Cooper'],
        genres=[],
        actors=[
            dict(
              id='637a59c5-8bf8-4d2c-a092-d8c6440cd7ed',
              name='George Cooper'
            )
        ],
        writers=[],
        directors=[]
    ),
    dict(
        id=UUID('830857b7-64d2-4a95-98c4-b03351daff52'),
        title='Robot Chicken: Star Wars III',
        imdb_rating=8.1,
        actors_names=['Abraham Benrubi'],
        description='The Emmy Award-winning Robot Chicken returns with its third send-up of the Star Wars universe! In this all-new hour-long special, four very different characters -- Emperor Palpatine, Darth Vader, Boba Fett and Gary the Stormtrooper -- reveal untold stories that weave and interconnect throughout all six Star Wars films! Set phasers to \'fun\'! Oh wait, that\'s the wrong franchise.',  # noqa
        genres=[],
        actors=[],
        writers=[],
        directors=[]
    ),
    dict(
        id=UUID('d1099968-805e-4a2b-a2ec-18bbde1201ac'),
        title='Robot Chicken: Star Wars Episode II',
        imdb_rating=8.1,
        actors_names=['Abraham Benrubi'],
        description='The second of three Star Wars themed Robot Chicken parodies.',
        genres=[],
        actors=[],
        writers=[],
        directors=[]
    ),
    dict(
        id=UUID('d77e45fc-2b84-442f-b652-caf31cb07c80'),
        title='Robot Chicken: Star Wars',
        imdb_rating=8.1,
        actors_names=['Abraham Benrubi'],
        description='The first of three Star Wars themed Robot Chicken parodies.',
        genres=[],
        actors=[],
        writers=[],
        directors=[]
    )
]
