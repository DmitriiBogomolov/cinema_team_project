import uuid

from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from sqlalchemy.exc import IntegrityError

from app.api.v1.catchers import default_exception_catcher
from app.schemas import UserSchema, BasicUserSchema
from app.exceptions import AlreadyExistsError
from app.models import User


users = Blueprint('users', __name__)


user_schema = UserSchema()
user_partial = BasicUserSchema(partial=True)


@users.route('', methods=('GET',))
@default_exception_catcher
def get_users() -> Tuple[Response, HTTPStatus]:
    users = User.get_list()
    return jsonify(user_schema.dump(users, many=True)), HTTPStatus.OK


@users.route('', methods=('POST',))
@default_exception_catcher
def create_user() -> Tuple[Response, HTTPStatus]:
    user = user_schema.load(request.get_json())
    try:
        result = user_schema.dump(user.save())
    except IntegrityError:
        raise AlreadyExistsError('Такой пользователь уже существует.')
    return jsonify(result), HTTPStatus.CREATED


@users.route('/<uuid:id>', methods=('PATCH',))
@default_exception_catcher
def update_user(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    valid_data = user_partial.load(request.get_json())
    try:
        user = User.update(id, valid_data)
    except IntegrityError:
        raise AlreadyExistsError('Такой пользователь уже существует.')
    return jsonify(user_schema.dump(user)), HTTPStatus.CREATED


@users.route('/<uuid:id>', methods=('DELETE',))
@default_exception_catcher
def delete_user(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    user = User.get_by_id(id)
    user.delete()
    return '', HTTPStatus.NO_CONTENT
