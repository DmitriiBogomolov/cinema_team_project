import uuid

from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from sqlalchemy.exc import IntegrityError

from app.api.v1.catchers import default_exception_catcher
from app.schemas import RoleSchema, BasicRoleSchema
from app.exceptions import AlreadyExistsError
from app.models import Role


roles = Blueprint('roles', __name__)


role_schema = RoleSchema()
role_partial = BasicRoleSchema(partial=True)


@roles.route('', methods=('GET',))
@default_exception_catcher
def get_roles() -> Tuple[Response, HTTPStatus]:
    roles = Role.get_list()
    return jsonify(role_schema.dump(roles, many=True)), HTTPStatus.OK


@roles.route('', methods=('POST',))
@default_exception_catcher
def create_role() -> Tuple[Response, HTTPStatus]:
    role = role_schema.load(request.get_json())
    try:
        result = role_schema.dump(role.save())
    except IntegrityError:
        raise AlreadyExistsError('Такая роль уже существует.')
    return jsonify(result), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('PATCH',))
@default_exception_catcher
def update_role(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    valid_data = role_partial.load(request.get_json())
    try:
        role = Role.update(id, valid_data)
    except IntegrityError:
        raise AlreadyExistsError('Такая роль уже существует.')
    return jsonify(role_schema.dump(role)), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('DELETE',))
@default_exception_catcher
def delete_role(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    role = Role.get_by_id(id)
    role.delete()
    return '', HTTPStatus.NO_CONTENT
