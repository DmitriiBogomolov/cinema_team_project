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
from app.models.core import EventAPI
from app.event_resolver import get_event_resolver, EventResolver
from app.handlers.manual_mail import (
    ManualMailHandler,
    ManualMailEvent,
    get_manual_mail_handler
)


router = APIRouter()


@router.post('')
async def load_event(
    event_data: EventAPI,
    auth: AuthJWT = Depends(),
    event_resolver: EventResolver = Depends(get_event_resolver)
) -> JSONResponse:
    """Обрабатывает автоматические и периодические события"""
    await authorize_service_token(auth)

    # Получаем соответствующий обработчик
    handler = await event_resolver.get_handler(event_data.event_name)

    # Передаем дальше
    await handler.handle(event_data)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'}
    )


@router.post('/send_manual')
async def send_manual(
    event_data: ManualMailEvent,
    auth: AuthJWT = Depends(),
    handler: ManualMailHandler = Depends(get_manual_mail_handler)
) -> JSONResponse:
    """Обрабатывает прямую рассылку уведомлений по переданному шаблону"""
    await authorize_service_token(auth)

    await handler.handle(event_data)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={'message': 'ok'}
    )
