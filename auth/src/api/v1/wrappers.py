from jwt.exceptions import DecodeError, ExpiredSignatureError
from http import HTTPStatus
from flask import jsonify, abort
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound

from src.exceptions import RevokedTokenError, AlreadyExistsError
from app import db


def default_exception_wrapper(func):
    """Basic exception wrapper for some views"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except DecodeError:
            return jsonify(message='Failed to parse jwt.'), HTTPStatus.BAD_REQUEST

        except RevokedTokenError:
            return jsonify(message='The token has been revoked.'), HTTPStatus.UNAUTHORIZED

        except ExpiredSignatureError:
            return jsonify(message='The token has expired.'), HTTPStatus.UNAUTHORIZED

        except NotFound:
            abort(404)

        except AlreadyExistsError as e:
            return jsonify(message=str(e)), HTTPStatus.CONFLICT

        except ValidationError as e:
            db.session.rollback()
            return jsonify({'message': e.messages}), HTTPStatus.UNPROCESSABLE_ENTITY

        except Exception:
            return jsonify(message='Something went wrong.'), HTTPStatus.INTERNAL_SERVER_ERROR

    wrapper.__name__ = func.__name__
    return wrapper
