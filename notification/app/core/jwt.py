from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from app.core.config import AppConfig, config


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


async def authorize_service_token(
        authorize: AuthJWT,
        roles: list | None = None
) -> dict | None:
    await authorize.jwt_required()
    current_subject = await authorize.get_jwt_subject()

    if config.debug:
        return current_subject

    if not current_subject.get('is_service'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The provided token is not service.'
        )

    jwt_roles = current_subject.get('roles', [])
    if roles and not any(role['name'] in roles for role in jwt_roles):
        # Проверяет, что в токене пользователя была представлена
        # хотя бы одна роль из списка roles (если он был передан)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient access rights.'
        )

    return current_subject
