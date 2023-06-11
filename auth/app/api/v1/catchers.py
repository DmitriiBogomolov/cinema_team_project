from http import HTTPStatus
from flask import jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound
import redis

from app.error_handlers.exceptions import (BaseAlreadyExists,
                                           BaseUnauthorized,
                                           NotFoundError,
                                           CaptchaError)
from app import db
from logger import logger


def default_exception_catcher(func):
    """Basic exception wrapper for some views"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NotFound as e:
            logger.error(e)
            e = NotFoundError()
            return jsonify(message=str(e.message)), HTTPStatus.NOT_FOUND

        except BaseAlreadyExists as e:
            logger.error(e)
            return jsonify(message=str(e)), HTTPStatus.CONFLICT

        except ValidationError as e:
            logger.error(e)
            db.session.rollback()
            return jsonify({'message': e.messages}), HTTPStatus.UNPROCESSABLE_ENTITY

        except BaseUnauthorized as e:
            logger.error(e)
            return jsonify({'message': e.message}), HTTPStatus.UNAUTHORIZED

        except CaptchaError as e:
            logger.error(e)
            return jsonify({'message': e.message}), HTTPStatus.UNPROCESSABLE_ENTITY

        except redis.exceptions.ConnectionError as e:
            raise e

        except Exception as e:
            logger.error(e)
            return jsonify(message='Something went wrong.'), HTTPStatus.INTERNAL_SERVER_ERROR

    wrapper.__name__ = func.__name__
    return wrapper
