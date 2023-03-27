from uuid import UUID

from src.models.person import Person as ModelPerson
from src.api.v1.response_models import PersonDetail as ResponsePerson

PERSONS_LIST = [
    dict(
        id=UUID('26ffbc3e-c539-11ed-afa1-0242ac120002'),
        full_name='Person',
        films=[]
    ),
    dict(
        id=UUID('26ffc094-c539-11ed-afa1-0242ac120002'),
        full_name='Person',
        films=[]
    ),
    dict(
        id=UUID('26ffc30a-c539-11ed-afa1-0242ac120002'),
        full_name='Person',
        films=[]
    ),
]

models = [ModelPerson(**item) for item in PERSONS_LIST]

response_models = [ResponsePerson(**item) for item in PERSONS_LIST]
