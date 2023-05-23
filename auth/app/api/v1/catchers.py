from http import HTTPStatus
from flask import jsonify, abort
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import NotFound

from app.exceptions import AlreadyExistsError
from app import db


def default_exception_catcher(func):
    """Basic exception wrapper for some views"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except NotFound:
            abort(404)

        except AlreadyExistsError as e:
            print(e)
            return jsonify(message=str(e)), HTTPStatus.CONFLICT

        except ValidationError as e:
            print(e)
            db.session.rollback()
            return jsonify({'message': e.messages}), HTTPStatus.UNPROCESSABLE_ENTITY

        except Exception as e:
            print(e)
            return jsonify(message='Something went wrong.'), HTTPStatus.INTERNAL_SERVER_ERROR

    wrapper.__name__ = func.__name__
    return wrapper
