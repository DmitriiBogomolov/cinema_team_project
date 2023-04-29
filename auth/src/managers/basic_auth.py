from flask import jsonify
from flask.wrappers import Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from src.models import User


def get_basic_auth() -> HTTPBasicAuth:
    """Provide configured HTTPBasicAuth"""

    basic_auth = HTTPBasicAuth()

    @basic_auth.error_handler
    def auth_error(status: int) -> Response:
        return jsonify(message='Unauthorized or wrong user credentials.'), status

    @basic_auth.verify_password
    def verify_password(username: str, password: str) -> Response:
        user = User.query.filter_by(email=username).first()
        if user and check_password_hash(user.password, password):
            return user

    return basic_auth
