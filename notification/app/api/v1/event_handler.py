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
from app.models.core import EventBase
from app.event_resolver import get_event_resolver


router = APIRouter()


@router.post('')
async def load_event(
    event_data: EventBase,
    auth: AuthJWT = Depends(),
    event_resolver = Depends(get_event_resolver)
) -> JSONResponse:
    """Загружает событие"""
    await authorize_service_token(auth)

    # Получаем соответствующий обработчик
    handler = await event_resolver.get_handler(event_data.event_name)

    # Передаем дальше
    await handler.handle(event_data)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'}
    )
