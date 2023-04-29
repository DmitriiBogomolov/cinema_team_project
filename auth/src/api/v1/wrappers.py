from jwt.exceptions import DecodeError, ExpiredSignatureError

from flask import jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import Unauthorized

from app import db
from src.services.jwt_service import RevokedTokenError


def default_exception_wrapper(func):
    """Basic exception wrapper for some views"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except DecodeError:
            return jsonify(message='Failed to parse jwt.'), 400

        except Unauthorized:
            return jsonify(message='Unauthorized or wrong user credentials.'), 401

        except RevokedTokenError:
            return jsonify(message='The token has been revoked.'), 401

        except ExpiredSignatureError:
            return jsonify(message='The token has expired.'), 401

        except ValidationError as e:
            db.session.rollback()
            return jsonify({'message': e.messages}), 422

        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(message='Something went wrong.'), 500

    wrapper.__name__ = func.__name__
    return wrapper
