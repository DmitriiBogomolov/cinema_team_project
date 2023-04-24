from flask import Blueprint, request, json, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                get_jwt)
from werkzeug.security import check_password_hash
from marshmallow.exceptions import ValidationError

from src.schemas import UserSchema, UserJWTPayloadSchema, SessionSchema
from src.models import User
from app import app, db, refresh_blacklist


auth = Blueprint('auth', __name__)

basic_auth = HTTPBasicAuth()


user_schema = UserSchema()
user_payload_schema = UserJWTPayloadSchema()
session_schema = SessionSchema()


@basic_auth.error_handler
def auth_error(status):
    return jsonify(message='Unauthorized or wrong user credentials.'), status


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if user and check_password_hash(user.password, password):
        return user


@auth.route('/register', methods=('POST',))
def register():
    try:
        json_data = json.loads(request.data)
        user = user_schema.load(json_data)

        if User.query.filter_by(email=user.email).first():
            return jsonify(message='User with that email already exists.'), 409

        db.session.add(user)
        db.session.commit()

        return jsonify(user_schema.dump(user)), 201

    except ValidationError as e:
        db.session.rollback()
        return jsonify(e.messages_dict), 400

    except Exception:
        db.session.rollback()
        return jsonify(message='Something went wrong.'), 500


@auth.route('/login', methods=('POST',))
@basic_auth.login_required
def login():
    try:
        user = basic_auth.current_user()
        user_payload = user_payload_schema.dump(user)

        access = create_access_token(identity=user_payload)
        refresh = create_refresh_token(identity=user_payload)

        session = session_schema.load({
            'user_id': user.id,
            'user_agent': request.user_agent,
            'remote_addr': request.environ['REMOTE_ADDR']
        })
        db.session.add(session)
        db.session.commit()

        return jsonify(
            access=access,
            refresh=refresh
        )

    except Exception as e:
        print(e)
        return jsonify(message='Something went wrong.'), 500


@auth.route('/logout', methods=('POST',))
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']
        refresh_blacklist.set(jti, '', ex=app.config['JWT_REFRESH_TOKEN_EXPIRES'])
        return jsonify(message='Refresh token revoked.')

    except Exception:
        return jsonify(message='Something went wrong.'), 500
