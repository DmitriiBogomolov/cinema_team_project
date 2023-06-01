from http import HTTPStatus

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import (jwt_required,
                                get_jwt,
                                current_user)

from app.api.v1.catchers import default_exception_catcher
from app.schemas import UserSchema, ProfileSchema, SignInEntrieSchema
from app.error_handlers.exceptions import UserAlreadyExists, UnavailableRefresh
from app.models import User
from app.jwt_service import jwt_service
from app.pre_configured.basic_auth import basic_auth


auth = Blueprint('auth', __name__)
user_schema = UserSchema()
profile_schema = ProfileSchema()


@auth.route('/register', methods=('POST',))
@default_exception_catcher
def user_registration() -> tuple[Response, HTTPStatus]:
    """
    Expected: JSON
        "email": "user@email.com",
        "password": "SD_g151@1af"
    """
    user = profile_schema.load(request.get_json())
    try:
        user.save()
    except IntegrityError:
        raise UserAlreadyExists
    return jsonify(profile_schema.dump(user)), HTTPStatus.CREATED


@auth.route('/login', methods=('POST',))
@basic_auth.login_required
@default_exception_catcher
def login() -> tuple[Response, HTTPStatus]:
    """
    Expected: Basic auth in headers
    """
    user = basic_auth.current_user()
    print(user)
    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    save_signin_entrie(user, request)
    return jsonify({'acsess': access, 'refresh': refresh}), HTTPStatus.OK


def save_signin_entrie(user: User, request: request):
    """Save a record to user log-in history"""
    schema = SignInEntrieSchema()
    entrie = schema.load({
        'user_id': user.id,
        'user_agent': request.user_agent.string,
        'remote_addr': request.environ['REMOTE_ADDR']
    })
    entrie.save()


@auth.route('/refresh', methods=('POST',))
@jwt_required(refresh=True)
@default_exception_catcher
def refresh() -> tuple[Response, HTTPStatus]:
    """
    Updates token pair
    Expected: Refresh token in header (Bearer refresh)
    """
    refresh = get_jwt()
    if jwt_service.verify_token(refresh):
        jwt_service.revoke_token(refresh)
        access, refresh = jwt_service.create_tokens(current_user)
        jwt_service.save_token(refresh)

        return jsonify({'acsess': access, 'refresh': refresh}), HTTPStatus.OK
    raise UnavailableRefresh


@auth.route('/logout', methods=('DELETE',))
@jwt_required(refresh=True)
@default_exception_catcher
def logout() -> tuple[Response, HTTPStatus]:
    """
    Logouts from current device.
    Expected: Refresh token in header (Bearer refresh)
    """
    refresh = get_jwt()
    if jwt_service.verify_token(refresh):
        jwt_service.revoke_token(refresh)
        return jsonify({'message': 'Успешный выход из аккаунта.'}), HTTPStatus.OK
    raise UnavailableRefresh


@auth.route('/logout_all', methods=('DELETE',))
@jwt_required()
@default_exception_catcher
def logout_all() -> tuple[Response, HTTPStatus]:
    """
    Logouts from all devices.
    Expected: Access token in header (Bearer access)
    """
    jwt_service.revoke_user_tokens(User)
    return jsonify({'message': 'Успешный выход из со всех устройств.'}), HTTPStatus.OK
