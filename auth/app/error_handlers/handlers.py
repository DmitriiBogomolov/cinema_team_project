from http import HTTPStatus
from werkzeug.exceptions import NotFound
from flask import jsonify, app

from logger import logger


def _handle_not_found(e: NotFound) -> None:
    logger.error(str(e))
    return jsonify(message=str(e)), HTTPStatus.NOT_FOUND


def register_error_handlers(app: app.Flask) -> None:
    app.register_error_handler(HTTPStatus.NOT_FOUND, _handle_not_found)
