from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError


class WrongEventException(Exception):
    pass


async def mongo_conflict_error(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={'message': 'Oops! This entity already exists.'}
    )


async def wrong_event_error(request: Request, exc: WrongEventException):
    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            'message': 'The event cannot be sent '
                       'according to the distribution policy.'
        }
    )


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(DuplicateKeyError, mongo_conflict_error)
    app.add_exception_handler(WrongEventException, wrong_event_error)
