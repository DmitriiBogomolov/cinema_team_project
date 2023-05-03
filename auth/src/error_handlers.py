from http import HTTPStatus
from werkzeug.exceptions import NotFound, Unauthorized
from flask import jsonify, app


def _handle_not_found(e: NotFound) -> None:
    return jsonify(message='Not found.'), HTTPStatus.BAD_REQUEST


def _handle_unauthorized(e: Unauthorized) -> None:
    return jsonify(message='Unauthorized or wrong user credentials.'), HTTPStatus.BAD_REQUEST


def register_error_handlers(app: app.Flask) -> None:
    app.register_error_handler(HTTPStatus.NOT_FOUND, _handle_not_found)
    app.register_error_handler(HTTPStatus.UNAUTHORIZED, _handle_unauthorized)
