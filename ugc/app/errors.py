from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError


async def mongo_conflict_error(request: Request, exc: DuplicateKeyError):
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={'message': 'Oops! This entity already exists.'}
    )


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(DuplicateKeyError, mongo_conflict_error)
