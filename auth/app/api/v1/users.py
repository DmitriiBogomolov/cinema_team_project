import uuid

from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

from app.api.v1.catchers import default_exception_catcher
from app.schemas import UserSchema, BasicUserSchema
from app.exceptions import AlreadyExistsError
from app.models import User, Role
from app.extensions import db


users = Blueprint('users', __name__)


user_schema = UserSchema()
user_partial = BasicUserSchema(partial=True)


@users.route('/<uuid:user_id>', methods=('GET',))
@jwt_required()
@default_exception_catcher
def get_user(user_id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """Getting all user data"""
    users = User.get_by_id(user_id)
    return jsonify(user_schema.dump(users)), HTTPStatus.OK


@users.route('', methods=('GET',))
@jwt_required()
@default_exception_catcher
def get_users_list() -> Tuple[Response, HTTPStatus]:
    """Getting all users list"""
    users = User.get_list()
    return jsonify(user_schema.dump(users, many=True)), HTTPStatus.OK


@users.route('', methods=('POST',))
@jwt_required()
@default_exception_catcher
def create_user() -> Tuple[Response, HTTPStatus]:
    """
    Extended user creation
    Expected: user model fields JSON
    """
    user = user_schema.load(request.get_json())
    try:
        result = user_schema.dump(user.save())
    except IntegrityError:
        raise AlreadyExistsError('Такой пользователь уже существует.')
    return jsonify(result), HTTPStatus.CREATED


@users.route('/<uuid:id>', methods=('PATCH',))
@jwt_required()
@default_exception_catcher
def update_user(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """
    Extended user update
    Expected: user model fields JSON
    """
    valid_data = user_partial.load(request.get_json())
    try:
        user = User.get_by_id(id)
        user.update(valid_data)
    except IntegrityError:
        raise AlreadyExistsError('Такой пользователь уже существует.')
    return jsonify(user_schema.dump(user)), HTTPStatus.OK


@users.route('/<uuid:id>', methods=('DELETE',))
@jwt_required()
@default_exception_catcher
def delete_user(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    user = User.get_by_id(id)
    user.delete()
    return '', HTTPStatus.NO_CONTENT


@users.route('/<uuid:user_id>/roles/<uuid:role_id>', methods=('POST',))
@jwt_required()
@default_exception_catcher
def set_role(user_id: uuid.UUID, role_id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """Sets the user to role."""
    user = User.get_by_id(user_id)
    role = Role.get_by_id(role_id)
    user.roles.append(role)
    db.session.commit()
    return jsonify(user_schema.dump(user)), HTTPStatus.OK


@users.route('/<uuid:user_id>/roles/<uuid:role_id>', methods=('POST',))
@jwt_required()
@default_exception_catcher
def revoke_role(user_id: uuid.UUID, role_id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """Revokes a user's role"""
    user = User.get_by_id(user_id)
    role = Role.get_by_id(role_id)
    user.roles.remove(role)
    db.session.commit()
    return jsonify(user_schema.dump(user)), HTTPStatus.OK
