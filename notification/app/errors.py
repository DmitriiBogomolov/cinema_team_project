from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class WrongEventException(Exception):
    pass


class WrongTemplateException(Exception):
    pass


async def wrong_event_error(request: Request, exc: WrongEventException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            'message': 'The event cannot be sent '
                       'according to the distribution policy.'
        }
    )


async def wrong_template_error(request: Request, exc: WrongTemplateException):
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content={
            'message': 'Wrong template.'
        }
    )


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(WrongEventException, wrong_event_error)
    app.add_exception_handler(WrongTemplateException, wrong_template_error)
