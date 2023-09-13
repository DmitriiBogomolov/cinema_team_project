"""
Эндпоинты для обработки поступающих событий
для последующей нотификации
"""
from http import HTTPStatus
from fastapi import (
    APIRouter, Depends
)
from typing import Union, List
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.core.jwt import authorize_service_token
from app.models import BasicEvent
from app.services.handler import AbstractHandler, get_handler


router = APIRouter()


@router.post('/event')
async def review_like_received(
    event: Union[BasicEvent, List[BasicEvent]],
    auth: AuthJWT = Depends(),
    handler: AbstractHandler = (
        Depends(get_handler)
    )
) -> JSONResponse:
    """
    Обрабатывает одно или пачку событий
    """
    await authorize_service_token(auth)
    await handler.handle_event(event)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=event.json()
    )
