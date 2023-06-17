from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from src.core.config import AppConfig


def configure_jwt(app: FastAPI) -> None:
    @AuthJWT.load_config
    def get_config():
        return AppConfig()

    @app.exception_handler(AuthJWTException)
    def authjwt_exception_handler(request: Request, exc: AuthJWTException):
        return JSONResponse(
            status_code=exc.status_code,
            content={'message': exc.message}
        )
