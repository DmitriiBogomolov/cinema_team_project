import uuid
from typing import Tuple
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_jwt_extended import jwt_required

from src.schemas import (RoleSchema,
                         UpdateRoleSchema
                         )
from src.api.v1.wrappers import default_exception_wrapper
from src.services.role_service import role_service

roles = Blueprint('roles', __name__)

role_schema = RoleSchema()
update_schema = UpdateRoleSchema()


@roles.route('', methods=('GET',))
@jwt_required()
@default_exception_wrapper
def get_role_data() -> Tuple[Response, HTTPStatus]:
    """Returns roles data"""
    roles = role_service.get_roles()
    return jsonify(role_schema.dump(roles, many=True)), HTTPStatus.OK


@roles.route('', methods=('POST',))
@jwt_required()
@default_exception_wrapper
def create_role_data() -> Tuple[Response, HTTPStatus]:
    """
    Creates role.
    Expected: JSON
        "name": "Модератор",
        "description": "Следит за соблюдением правил ресурса в конкретных темах или разделах сетевого ресурса"
    """
    data = request.get_json()
    role = role_service.create_role(data)
    return jsonify(role_schema.dump(role)), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('PATCH',))
@jwt_required()
@default_exception_wrapper
def update_role_data(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """
    Partially updates role
    Expected: JSON
        "name": "Модератор",
        "description": "Следит за соблюдением правил ресурса в конкретных темах или разделах сетевого ресурса"
    """
    data = request.get_json()
    role = role_service.update_role(id, data)
    return jsonify(role_schema.dump(role)), HTTPStatus.CREATED


@roles.route('/<uuid:id>', methods=('DELETE',))
@jwt_required()
@default_exception_wrapper
def delete_role_data(id: uuid.UUID) -> Tuple[Response, HTTPStatus]:
    """
    Removes role.
    """
    role_service.delete_role(id)
    return jsonify({'message': 'OK'}), HTTPStatus.OK
