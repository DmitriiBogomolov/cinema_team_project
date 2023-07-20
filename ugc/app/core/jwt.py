from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from app.core.config import AppConfig


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


def access_check(current_user: dict, roles: list = []) -> dict | None:
    """Проверка достаточности прав доступа для jwt_subject"""

    if not current_user.get('is_active'):
        #  Проверяет, что пользователь активен
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The provided user is inactive'
        )

    jwt_roles = current_user.get('roles', [])

    if roles and not any(role['name'] in roles for role in jwt_roles):
        #  Проверяет, что в токене пользователя была представлена
        #  хотя бы одна роль из списка roles (если он был передан)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient access rights.'
        )

    return current_user
