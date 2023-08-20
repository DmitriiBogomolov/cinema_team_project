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
from app.models import BasicEvent
from app.services.handler import AbstractHandler, get_handler


router = APIRouter()


@router.post('/single_event')
async def review_like_received(
    event: BasicEvent,
    auth: AuthJWT = Depends(),
    handler: AbstractHandler = (
        Depends(get_handler)
    )
) -> JSONResponse:
    """
    Обрабатывает одиночное событие нового
    лайка на review пользователя
    """
    await authorize_service_token(auth)
    await handler.handle_single(event)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=event.json()
    )


@router.post('/multi_events')
async def mail_multiple(
    events: list[BasicEvent],
    auth: AuthJWT = Depends(),
    handler: AbstractHandler = (
        Depends(get_handler)
    )
) -> JSONResponse:
    """Обрабатывает множественную рассылку по предложенному шаблону"""
    await authorize_service_token(auth)
    await handler.handle_multi(events)
    return events
