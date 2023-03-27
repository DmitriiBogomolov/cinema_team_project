from uuid import UUID

from src.models.genre import Genre as ModelGenre
from src.api.v1.response_models import Genre as ResponseGenre


GENRES_LIST = [
    dict(
        id=UUID('26ffbc3e-c539-11ed-afa1-0242ac120002'),
        name='Genre 1',
        description='Test'
    ),
    dict(
        id=UUID('26ffc094-c539-11ed-afa1-0242ac120002'),
        name='Genre 2'
    ),
    dict(
        id=UUID('26ffc30a-c539-11ed-afa1-0242ac120002'),
        name='Genre 3',
        description='Test'
    ),
]

models = [ModelGenre(**item) for item in GENRES_LIST]

response_models = [ResponseGenre(**item) for item in GENRES_LIST]
