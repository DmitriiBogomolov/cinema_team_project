from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_jwt_extended import jwt_required, current_user
from werkzeug.security import check_password_hash
from marshmallow.exceptions import ValidationError

from src.schemas import (UserSchema,
                         UpdateUserSchema,
                         OutputEntrieSchema,
                         ChangePasswordSchema)
from src.models import LoginEntrie, User
from app import db


users = Blueprint('users', __name__)

user_schema = UserSchema()
update_schema = UpdateUserSchema()


@users.route('/me', methods=('GET',))
@jwt_required()
def get_user_data() -> Response:
    """Provide user data"""
    try:
        return jsonify(user_schema.dump(current_user)), 201
    except Exception:
        return jsonify(message='Something went wrong.'), 500


@users.route('/me', methods=('PATCH',))
@jwt_required()
def update_user_data() -> Response:
    """
    Partially updates user data
    Expected: JSON
    {
    "email": "user@email.com"
    }
    """
    try:
        data = request.get_json()
        valid_data = update_schema.load(data)

        if User.query.filter_by(email=valid_data['email']).first():
            return jsonify(message='User with that email already exists.'), 409

        current_user.email = valid_data['email']
        db.session.commit()

        return jsonify(user_schema.dump(current_user)), 201

    except ValidationError as e:
        db.session.rollback()
        return jsonify({'message': e.messages}), 422
    except Exception:
        return jsonify(message='Something went wrong.'), 500


@users.route('/me/history', methods=('GET',))
@jwt_required()
def get_user_history() -> Response:
    """Provides user log-in history"""
    try:
        entries = (LoginEntrie.query.filter_by(user_id=current_user.id)
                                    .order_by(LoginEntrie.created.desc()))
        schema = OutputEntrieSchema(many=True)
        return jsonify(schema.dump(entries)), 200

    except Exception:
        return jsonify(message='Something went wrong.'), 500


@users.route('/me/change_password', methods=('POST',))
@jwt_required()
def change_password() -> Response:
    """
    Expected: JSON
    {
        "password": "AFaf@Sfa12$@1",
        "new_password": "AFaf@Sfa12$@",
        "new_password_re": "AFaf@Sfa12$@"
    }
    """
    try:
        data = request.get_json()

        password_schema = ChangePasswordSchema()

        valid_data = password_schema.load(data)

        if not check_password_hash(current_user.password, valid_data['password']):
            return jsonify({'message': 'Current password is wrong.'}), 401

        current_user.password = UserSchema.get_password_hash(valid_data['new_password'])
        db.session.commit()

        return jsonify({'message': 'OK'}), 200

    except ValidationError as e:
        db.session.rollback()
        return jsonify(message=e.messages_dict), 422
    except Exception:
        return jsonify(message='Something went wrong.'), 500
