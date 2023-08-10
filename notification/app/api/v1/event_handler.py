"""
Эндпоинты для обработки поступающих событий
для последующей нотификации
"""

from fastapi import (
    APIRouter, Depends
)
from async_fastapi_jwt_auth import AuthJWT
from fastapi.responses import JSONResponse

from app.core.jwt import authorize_service_token
from app.models import (
    SingleNewReviewLike,
    MultipleTemplateMailing,
    MultipleBookmarksReminder,
    ConfirmLetter)
from app.services.sheduler import AbstractSheduler, get_sheduler


router = APIRouter()


@router.post('/review_like_received')
async def review_like_received(
    event: SingleNewReviewLike,
    auth: AuthJWT = Depends(),
    sheduler: AbstractSheduler = (
        Depends(get_sheduler)
    )
) -> JSONResponse:
    """
    Обрабатывает одиночное событие нового
    лайка на review пользователя
    """
    await authorize_service_token(auth)
    await sheduler.handle_single(event)

    return event
    #  return JSONResponse(
    #      status_code=HTTPStatus.OK,
    #      content={'message': 'The event is accepted for processing.'}
    #  )


@router.post('/mail_multiple')
async def mail_multiple(
    event: MultipleTemplateMailing,
    auth: AuthJWT = Depends(),
    sheduler: AbstractSheduler = (
        Depends(get_sheduler)
    )
) -> JSONResponse:
    """Обрабатывает множественную рассылку по предложенному шаблону"""
    await authorize_service_token(auth)
    await sheduler.handle_multiple(event)
    return event


@router.post('/bookmarks_reminder_multiple')
async def bookmarks_reminder_multiple(
    event: MultipleBookmarksReminder,
    auth: AuthJWT = Depends(),
    sheduler: AbstractSheduler = (
        Depends(get_sheduler)
    )
) -> JSONResponse:
    """
    Обрабатывает множественную рассылку уведомлений
    об отложенных фильмах
    """
    await authorize_service_token(auth)
    await sheduler.handle_multiple(event)
    return event


@router.post('/confirm_letter')
async def confirm_letter(
    event: ConfirmLetter,
    auth: AuthJWT = Depends(),
    sheduler: AbstractSheduler = (
        Depends(get_sheduler)
    )
) -> JSONResponse:
    await authorize_service_token(auth)
    await sheduler.handle_single(event)
    print(event)
    return event
