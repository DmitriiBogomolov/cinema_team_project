from flask import Blueprint, request, json, jsonify
from flask.wrappers import Response
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                decode_token)
from marshmallow.exceptions import ValidationError

from src.schemas import UserSchema, UserJWTPayloadSchema, LoginEntrieSchema
from src.models import User
from app import app, db, refresh_blacklist, basic_auth


auth = Blueprint('auth', __name__)

user_schema = UserSchema()
user_payload_schema = UserJWTPayloadSchema()  # repr user data in jwt
entrie_schema = LoginEntrieSchema()  # repr one record of logins history


@auth.route('/register', methods=('POST',))
def register() -> Response:
    """
    Register new user.
    Expected: JSON
    {
        "email": "user@email.com",
        "password": "SD_g151@1af"
    }
    """
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
        return jsonify({'message': e.messages}), 400

    except Exception:
        db.session.rollback()
        return jsonify(message='Something went wrong.'), 500


@auth.route('/login', methods=('POST',))
@basic_auth.login_required
def login() -> Response:
    """
    Provides a token pair using BasicAuth login/password credentials.
    Expected: None
    """
    try:
        user = basic_auth.current_user()

        user_payload = user_payload_schema.dump(user)

        access = create_access_token(identity=user_payload)
        refresh = create_refresh_token(identity=user_payload)

        entrie = entrie_schema.load({
            'user_id': user.id,
            'user_agent': request.user_agent,
            'remote_addr': request.environ['REMOTE_ADDR']
        })
        db.session.add(entrie)
        db.session.commit()

        return jsonify(
            access=access,
            refresh=refresh
        )

    except Exception:
        return jsonify(message='Something went wrong.'), 500


@auth.route('/logout', methods=('POST',))
@jwt_required()
def logout() -> Response:
    """
    Revoke the provided refresh token.
    Expected: JSON
    {
        "refresh": "eyJhb...GciOi...JIUzI1"
    }
    """
    try:
        refresh = decode_token(json.loads(request.data)['refresh'])
        jti = refresh['jti']

        if refresh_blacklist.exists(jti):
            return jsonify(message='This token has already been revoked.'), 400

        refresh_blacklist.set(jti, '', ex=app.config['JWT_REFRESH_TOKEN_EXPIRES'])
        return jsonify(message='Successfully revoked.'), 200

    except Exception:
        return jsonify(message='Something went wrong.'), 500
