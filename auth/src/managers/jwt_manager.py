from flask import jsonify
from flask_jwt_extended import JWTManager


def get_jwt_manager(app):
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(message='Expired'), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(jwt_header):
        return jsonify(message='Invalid'), 401

    @jwt.token_verification_failed_loader
    def token_verification_failed(jwt_header):
        return jsonify(message='WTF???'), 401

    @jwt.unauthorized_loader
    def no_jwt_cb(jwt_header):
        return jsonify(message='No jwt'), 401

    return jwt
