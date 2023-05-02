from werkzeug.exceptions import NotFound, Unauthorized
from flask import jsonify, app


def _handle_not_found(e: NotFound) -> None:
    return jsonify(message='Not found.'), 400


def _handle_unauthorized(e: Unauthorized) -> None:
    return jsonify(message='Unauthorized or wrong user credentials.'), 400


def register_error_handlers(app: app.Flask) -> None:
    app.register_error_handler(404, _handle_not_found)
    app.register_error_handler(401, _handle_unauthorized)
