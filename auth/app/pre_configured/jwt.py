from http import HTTPStatus
from flask import jsonify, app
from flask.wrappers import Response
from flask_jwt_extended import JWTManager

from app.models import User


def init_jwt_manager(app: app.Flask) -> JWTManager:
    """Provide configured JWTManager"""

    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header: dict, _jwt_data: dict) -> Response:
        user_id = _jwt_data['sub']['id']
        return User.query.filter_by(id=user_id).one_or_none()

    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header: dict, _jwt_payload: dict) -> Response:
        return jsonify(message='Provided JWT expired'), HTTPStatus.UNAUTHORIZED

    @jwt.invalid_token_loader
    def invalid_token_callback(_jwt_header: dict) -> Response:
        return jsonify(message='Invalid token provided'), HTTPStatus.UNAUTHORIZED

    @jwt.token_verification_failed_loader
    def token_verification_failed(_jwt_header: dict) -> Response:
        return jsonify(message='Get off the site, scammer!'), HTTPStatus.UNAUTHORIZED

    @jwt.unauthorized_loader
    def no_jwt_cb(_jwt_header: dict) -> Response:
        return jsonify(message='No JWT provided.'), HTTPStatus.UNAUTHORIZED

    return jwt
