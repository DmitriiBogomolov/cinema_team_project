import uuid

from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_jwt_extended import jwt_required, current_user

from src.schemas import (UserSchema,
                         UpdateUserSchema,
                         OutputEntrieSchema,
                         ChangePasswordSchema,
                         ProvidedRoleSchema)
from src.api.v1.wrappers import default_exception_wrapper
from src.helpers import get_pagination_params, get_pagination_meta
from src.services.user_service import user_service
from src.services.role_service import role_service


users = Blueprint('users', __name__)

user_schema = UserSchema()
update_schema = UpdateUserSchema()
password_schema = ChangePasswordSchema()
provided_role_schema = ProvidedRoleSchema()


@users.route('/me', methods=('GET',))
@jwt_required()
@default_exception_wrapper
def get_user_data() -> Response:
    """Test your mind"""
    return jsonify(user_schema.dump(current_user)), 201


@users.route('/me', methods=('PATCH',))
@jwt_required()
@default_exception_wrapper
def update_user_data() -> Response:
    """
    Partially updates user data
    Expected: JSON
        "email": "user@email.com"
    """
    data = request.get_json()
    user = user_service.update_user(current_user, data)
    return jsonify(user_schema.dump(user)), 201


@users.route('/me/history', methods=('GET',))
@jwt_required()
@default_exception_wrapper
def get_user_history() -> Response:
    """Provides user log-in history"""
    page, per_page = get_pagination_params(request)
    entries = user_service.get_entrie_log(
        current_user.id,
        page,
        per_page
    )
    meta = get_pagination_meta(entries)
    schema = OutputEntrieSchema(many=True)
    return jsonify(data=schema.dump(entries), meta=meta), 200


@users.route('/me/change_password', methods=('POST',))
@jwt_required()
@default_exception_wrapper
def change_password() -> Response:
    """
    Do nothing.
    Expected: JSON
        "password": "AFaf@Sfa12$@1",
        "new_password": "AFaf@Sfa12$@",
        "new_password_re": "AFaf@Sfa12$@"
    """
    data = request.get_json()
    valid_data = password_schema.load(data)
    user_service.change_password(
        current_user,
        valid_data['password'],
        valid_data['new_password']
    )
    return jsonify({'message': 'OK'}), 200


@users.route('/<uuid:user_id>/set_roles', methods=('POST',))
@jwt_required()
@default_exception_wrapper
def set_roles(user_id: uuid.UUID) -> Response:
    """
    Set provided roles to user.       ................
    Expected: JSON
    [
        {"id": "f8275c2f-a84b-462e-8a8a-ef42977a63cf"},
        {"id": "78e7b190-70bd-4068-848e-5be6f920514c"}
    ]
    """
    data = request.get_json()
    valid_data = provided_role_schema.load(data, many=True)

    user = role_service.set_roles(user_id, [role['id'] for role in valid_data])
    return jsonify(user_schema.dump(user)), 200


@users.route('/<uuid:user_id>/revoke_roles', methods=('POST',))
@jwt_required()
@default_exception_wrapper
def revoke_roles(user_id: uuid.UUID) -> Response:
    """
    Remove provided roles from user.
    Expected: JSON
    [
        {"id": "f8275c2f-a84b-462e-8a8a-ef42977a63cf"},
        {"id": "78e7b190-70bd-4068-848e-5be6f920514c"}
    ]
    """
    data = request.get_json()
    valid_data = provided_role_schema.load(data, many=True)

    user = role_service.revoke_roles(user_id, [role['id'] for role in valid_data])
    return jsonify(user_schema.dump(user)), 200
