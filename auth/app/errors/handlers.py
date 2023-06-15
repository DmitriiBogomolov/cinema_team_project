from http import HTTPStatus
from werkzeug.exceptions import NotFound
from flask import jsonify, app
import sqlalchemy
import redis

from app.core.logger import logger


def _handle_not_found(e: NotFound) -> None:
    logger.error(str(e))
    return jsonify(message=str(e)), HTTPStatus.NOT_FOUND


def _handle_lose_postgres_connection(e: sqlalchemy.exc.OperationalError):
    logger.error(str(e))
    return jsonify({'message': 'Something went wrong. (code: 1)'}), 500


def _handle_lose_redis_connection(e: redis.exceptions.ConnectionError):
    logger.error(str(e))
    return jsonify({'message': 'Something went wrong. (code: 2)'}), 500


def register_error_handlers(app: app.Flask) -> None:
    app.register_error_handler(HTTPStatus.NOT_FOUND, _handle_not_found)
    app.register_error_handler(
        sqlalchemy.exc.OperationalError,
        _handle_lose_postgres_connection
    )
    app.register_error_handler(
        redis.exceptions.ConnectionError,
        _handle_lose_redis_connection
    )
