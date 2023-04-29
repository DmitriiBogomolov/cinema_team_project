from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_jwt_extended import jwt_required, current_user

from src.schemas import (UserSchema,
                         UpdateUserSchema,
                         OutputEntrieSchema,
                         ChangePasswordSchema)
from src.api.v1.wrappers import default_exception_wrapper
from src.services.user_service import user_service, AlreadyExistsError


users = Blueprint('users', __name__)

user_schema = UserSchema()
update_schema = UpdateUserSchema()
password_schema = ChangePasswordSchema()


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
    try:
        data = request.get_json()
        user = user_service.update_user(current_user, data)
        return jsonify(user_schema.dump(user)), 201

    except AlreadyExistsError:
        return jsonify(message='User with that email already exists.'), 409


@users.route('/me/history', methods=('GET',))
@jwt_required()
@default_exception_wrapper
def get_user_history() -> Response:
    """Provides user log-in history"""
    entries = user_service.get_entrie_log(current_user.id)
    schema = OutputEntrieSchema(many=True)
    return jsonify(schema.dump(entries)), 200


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
