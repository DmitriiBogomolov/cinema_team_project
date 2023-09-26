"""
Эндпоинты для обработки поступающих событий
для последующей нотификации
"""
from http import HTTPStatus
from fastapi import (
    APIRouter, Depends
)
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.core.jwt import authorize_service_token
from app.base_models import BasicEvent
from app.event_resolver import get_event_handler


router = APIRouter()


@router.post('')
async def load_events(
    event_data: BasicEvent,
    auth: AuthJWT = Depends()
) -> JSONResponse:
    """
    Для отправки пачки однородных событий 
    """
    await authorize_service_token(auth)

    handler = get_event_handler(event_data.event_name)

    await handler.handle(event_data)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'}
    )
