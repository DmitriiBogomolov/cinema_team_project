"""Сохраняет события просмотров"""

import json
from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi_request_id import get_request_id
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse
from aiokafka import AIOKafkaProducer
from redis.asyncio import Redis

from app.request_models import RequestViewEventModel
from app.db.kafka import get_kafka_producer
from app.db.redis import get_redis
from app.core.jwt import authorize_for_roles
from app.core.logger import logger


router = APIRouter()


@router.post('')
async def load_event(
    view_event: RequestViewEventModel,
    auth: AuthJWT = Depends(),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
    redis: Redis = Depends(get_redis)
) -> JSONResponse:
    """Сохраняет событие просмотра в кафку"""
    current_user = await authorize_for_roles(auth)

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

    await producer.send_and_wait(topic='views', key=key, value=value)
    await redis.set(key, value)
    logger.info('data loading completed', extra={'request_id': get_request_id()})
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'}
    )
