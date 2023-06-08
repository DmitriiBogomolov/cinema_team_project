import uuid

from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from sqlalchemy.exc import IntegrityError

from app.api.v1.catchers import default_exception_catcher
from app.schemas import RoleSchema, BasicRoleSchema
from app.error_handlers.exceptions import BaseAlreadyExists
from app.models import Role
from app.pre_configured.jwt_wrappers import jwt_roles_required


roles = Blueprint('roles', __name__)


role_schema = RoleSchema()
role_partial = BasicRoleSchema(partial=True)


@roles.route('', methods=('GET',))
@jwt_roles_required('manager')
@default_exception_catcher
def get_roles() -> tuple[Response, HTTPStatus]:
    """Getting all roles"""
    roles = Role.get_list()
    return jsonify(role_schema.dump(roles, many=True)), HTTPStatus.OK


@roles.route('', methods=('POST',))
@jwt_roles_required('manager')
@default_exception_catcher
def create_role() -> tuple[Response, HTTPStatus]:
    """
    Expected: JSON
        "name": "moderator",
        "description": "do something",
    """
    role = role_schema.load(request.get_json())
    try:
        result = role_schema.dump(role.save())
    except IntegrityError:
        raise BaseAlreadyExists
    return jsonify(result), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('PATCH',))
@jwt_roles_required('manager')
@default_exception_catcher
def update_role(id: uuid.UUID) -> tuple[Response, HTTPStatus]:
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
        raise BaseAlreadyExists
    return jsonify(role_schema.dump(role)), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('DELETE',))
@jwt_roles_required('manager')
@default_exception_catcher
def delete_role(id: uuid.UUID) -> tuple[Response, HTTPStatus]:
    role = Role.get_by_id(id)
    role.delete()
    return '', HTTPStatus.NO_CONTENT
