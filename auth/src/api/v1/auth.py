from flask import Blueprint, request, json, jsonify
from flask.wrappers import Response
from flask_jwt_extended import (jwt_required,
                                decode_token)

from src.schemas import UserSchema, UserJWTPayloadSchema, LoginEntrieSchema
from src.api.v1.wrappers import default_exception_wrapper
from src.services.jwt_service import jwt_service
from src.services.user_service import user_service, AlreadyExistsError
from app import basic_auth

auth = Blueprint('auth', __name__)

user_schema = UserSchema()
user_payload_schema = UserJWTPayloadSchema()  # repr user data in jwt
entrie_schema = LoginEntrieSchema()  # repr one record of logins history


@auth.route('/register', methods=('POST',))
@default_exception_wrapper
def register() -> Response:
    """
    Register new user.
    Expected: JSON
        "email": "user@email.com",
        "password": "SD_g151@1af"
    """
    try:
        json_data = json.loads(request.data)
        user = user_service.create_user(json_data)
        return jsonify(user_schema.dump(user)), 201

    except AlreadyExistsError:
        return jsonify(message='User with that email already exists.'), 409


@auth.route('/login', methods=('POST',))
@basic_auth.login_required
@default_exception_wrapper
def login() -> Response:
    """
    Provides a token pair using BasicAuth login/password credentials.
    Expected: None
    """
    user = basic_auth.current_user()
    tokens = jwt_service.create_jwt_pair(user)
    user_service.save_entrie_log(user.id, request)

    return jsonify(**tokens), 200


@auth.route('/refresh', methods=('POST',))
@default_exception_wrapper
def refresh() -> Response:
    """
    Get new token pair.
    Expected: JSON
        "refresh": "eyJhb...GciOi...JIUzI1"
    """
    refresh = decode_token(json.loads(request.data)['refresh'])
    return jsonify(**jwt_service.refresh_jwt_pair(refresh)), 200


@auth.route('/logout', methods=('POST',))
@jwt_required()
@default_exception_wrapper
def logout() -> Response:
    """
    Revoke the provided refresh token.
    Expected: JSON
        "refresh": "eyJhb...GciOi...JIUzI1"
    }
    """
    refresh = decode_token(json.loads(request.data)['refresh'])
    jwt_service.revoke_token(refresh)
    return jsonify(message='Successfully revoked.'), 200
