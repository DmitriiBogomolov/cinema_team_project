from typing import Tuple
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import decode_token
from app.api.v1.catchers import default_exception_catcher
from app.schemas import UserSchema
from app.exceptions import AlreadyExistsError
from app.models import User
from app.jwt_service import jwt_service
from pydantic import BaseModel


auth = Blueprint('auth', __name__)
user_schema = UserSchema()


# модель заглушка для проверки ручек
class UserAuth(BaseModel):
    id: str
    email: str
    password: str


@auth.route('/register', methods=('POST',))
@default_exception_catcher
def user_registration() -> Tuple[Response, HTTPStatus]:
    user = user_schema.load(request.get_json())
    try:
        result = user_schema.dump(user.save())
    except IntegrityError:
        raise AlreadyExistsError('Такой пользователь уже существует.')
    return jsonify(result), HTTPStatus.CREATED


@auth.route('/login', methods=('POST',))
@default_exception_catcher
def login() -> Tuple[Response, HTTPStatus]:
    user_data = request.get_json()
    query = User.find_by_email(email=user_data['email'])
    user = UserAuth(**user_schema.dump(query)).dict()
    try:
        if user_schema.verify_hash(user['password'], user_data['password']):
            access_token, refresh_token = jwt_service.create_tokens(user)
            jwt_service.save_token(refresh_token)
        else:
            raise AlreadyExistsError('Неверный пароль')
    except KeyError:
        raise AlreadyExistsError('Пользователь не найден')
    return jsonify({'acsess_token': access_token, 'refresh_token': refresh_token}), HTTPStatus.OK


@auth.route('/refresh', methods=('POST',))
@default_exception_catcher
def update_refresh() -> Tuple[Response, HTTPStatus]:
    data_user = request.get_json()
    user = decode_token(data_user['refresh'])['sub']

    if jwt_service.verify_token(data_user['refresh']):
        jwt_service.revoke_token(data_user['refresh'])
        access_token, refresh_token = jwt_service.create_tokens(user)
        jwt_service.save_token(refresh_token)

        return jsonify({'acsess_token': access_token, 'refresh_token': refresh_token}), HTTPStatus.OK
    else:
        raise AlreadyExistsError('Токен недействительный')


@auth.route('/logout', methods=('POST',))
@default_exception_catcher
def logout() -> Tuple[Response, HTTPStatus]:
    data_user = request.get_json()
    if jwt_service.verify_token(data_user['refresh']):
        jwt_service.revoke_token(data_user['refresh'])
        return jsonify({'message': 'Успешный выход из аккаунта.'}), HTTPStatus.OK
    else:
        return jsonify(''), HTTPStatus.CONFLICT


@auth.route('/logout_all', methods=('POST',))
@default_exception_catcher
def logout_all() -> Tuple[Response, HTTPStatus]:
    data_user = request.get_json()
    if jwt_service.verify_token(data_user['refresh']):
        jwt_service.revoke_token(data_user['refresh'], all=True)
        return jsonify({'message': 'Успешный выход из аккаунта.'}), HTTPStatus.OK
