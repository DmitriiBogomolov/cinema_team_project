import uuid

from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required

from app.api.v1.catchers import default_exception_catcher
from app.schemas import RoleSchema, BasicRoleSchema
from app.exceptions import AlreadyExistsError
from app.models import Role


roles = Blueprint('roles', __name__)


role_schema = RoleSchema()
role_partial = BasicRoleSchema(partial=True)


@roles.route('', methods=('GET',))
@jwt_required()
@default_exception_catcher
def get_roles() -> Tuple[Response, HTTPStatus]:
    """Getting all roles"""
    roles = Role.get_list()
    return jsonify(role_schema.dump(roles, many=True)), HTTPStatus.OK


@roles.route('', methods=('POST',))
@jwt_required()
@default_exception_catcher
def create_role() -> Tuple[Response, HTTPStatus]:
    """
    Expected: JSON
        "name": "moderator",
        "description": "do something",
    """
    role = role_schema.load(request.get_json())
    try:
        result = role_schema.dump(role.save())
    except IntegrityError:
        raise AlreadyExistsError('Такая роль уже существует.')
    return jsonify(result), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('PATCH',))
@jwt_required()
@default_exception_catcher
def update_role(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """
    Expected: JSON
        "name": "moderator",
        "description": "do something",
    """
    role = Role.get_by_id(id)
    valid_data = role_partial.load(request.get_json())
    try:
        role.update(valid_data)
    except IntegrityError:
        raise AlreadyExistsError('Роль уже существует.')
    return jsonify(role_schema.dump(role)), HTTPStatus.OK


@roles.route('/<uuid:id>', methods=('DELETE',))
@jwt_required()
@default_exception_catcher
def delete_role(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    role = Role.get_by_id(id)
    role.delete()
    return '', HTTPStatus.NO_CONTENT
