from flask_httpauth import HTTPTokenAuth
from flask.wrappers import Response
from flask import abort

from app.models import ServiceToken


def get_token_auth() -> HTTPTokenAuth:

    token_auth = HTTPTokenAuth(scheme='Bearer')

    @token_auth.error_handler
    def auth_error(status: int) -> Response:
        abort(401)

    @token_auth.verify_token
    def verify_token(token):
        service = ServiceToken.get_by_token(token)
        if service:
            return service

    return token_auth


token_auth = get_token_auth()
