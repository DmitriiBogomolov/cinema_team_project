from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_jwt_extended import jwt_required, current_user

from src.schemas import (RoleSchema,
                         UpdateRoleSchema
                         )
from src.api.v1.wrappers import default_exception_wrapper
from src.services.role_service import role_service, AlreadyExistsError

roles = Blueprint('roles', __name__)

role_schema = RoleSchema()
update_schema = UpdateRoleSchema()


@roles.route('/me', methods=('GET',))
@jwt_required()
@default_exception_wrapper
def get_role_data() -> Response:
    """Returns roles data"""
    return jsonify(role_schema.dump(current_user)), 201


@roles.route('/me', methods=('PATCH',))
@jwt_required()
@default_exception_wrapper
def update_role_data() -> Response:
    """
    Partially updates role
    Expected: JSON
        "name": "Модератор",
        "description": "Следит за соблюдением правил ресурса в конкретных темах или разделах сетевого ресурса"
    """
    try:
        data = request.get_json()
        role = role_service.update_role(current_user, data)
        return jsonify(role_schema.dump(role)), 201

    except AlreadyExistsError:
        return jsonify(message='Role already exists.'), 409


@roles.route('/me', methods=('POST',))
@jwt_required()
@default_exception_wrapper
def create_role_data() -> Response:
    """
    Creates role.
    Expected: JSON
        "id": "6931c67c-d85f-11ed-afa1-0242ac120002",
        "name": "Модератор",
        "description": "Следит за соблюдением правил ресурса в конкретных темах или разделах сетевого ресурса"
    """
    try:
        data = request.get_json()
        role = role_service.create_role(current_user, data)
        return jsonify(role_schema.dump(role)), 201

    except AlreadyExistsError:
        return jsonify(message='Role already exists.'), 409


@roles.route('/me', methods=('DELETE',))
@jwt_required()
@default_exception_wrapper
def delete_role_data() -> Response:
    """
    Removes role.
    """
    data = request.get_json()
    role_service.delete_role(current_user, data)
    return jsonify({'message': 'OK'}), 200
