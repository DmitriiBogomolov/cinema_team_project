import json
from datetime import datetime

from fastapi import APIRouter, Depends
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from kafka import KafkaProducer

from src.models import ViewEventModel
from src.core.jwt import access_check
from src.core.config import kafka_config


router = APIRouter()

producer = KafkaProducer(bootstrap_servers=f'{kafka_config.host}:{kafka_config.port}')


@router.post('')
async def load_event(
    view_event: ViewEventModel,
    authorize: AuthJWT = Depends()
) -> JSONResponse:

    await authorize.jwt_required()
    current_user = access_check(
        await authorize.get_jwt_subject()
    )

    key = bytes(f'{current_user["id"]},{str(view_event.movie_id)}', encoding='utf-8')
    value = bytes(
        json.dumps(
            {
                'user_id': str(current_user['id']),
                'movie_id': str(view_event.movie_id),
                'duration': view_event.duration,
                'lenght_movie': view_event.lenght_movie,
                'event_time': int(datetime.timestamp(datetime.now()))
            }
        ),
        encoding='utf-8'
    )

    producer.send(topic='views', key=key, value=value)

    return JSONResponse(
        status_code=200,
        content={'message': 'ok'}
    )
