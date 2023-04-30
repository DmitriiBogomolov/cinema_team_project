from jwt.exceptions import DecodeError, ExpiredSignatureError

from flask import jsonify
from marshmallow.exceptions import ValidationError

from src.exceptions import RevokedTokenError, AlreadyExistsError
from app import db


def default_exception_wrapper(func):
    """Basic exception wrapper for some views"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except DecodeError:
            return jsonify(message='Failed to parse jwt.'), 400

        except RevokedTokenError:
            return jsonify(message='The token has been revoked.'), 401

        except ExpiredSignatureError:
            return jsonify(message='The token has expired.'), 401

        except AlreadyExistsError as e:
            return jsonify(message=str(e)), 409

        except ValidationError as e:
            db.session.rollback()
            return jsonify({'message': e.messages}), 422

        except Exception as e:
            print(e)
            return jsonify(message='Something went wrong.'), 500

    wrapper.__name__ = func.__name__
    return wrapper
