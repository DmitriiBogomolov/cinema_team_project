from typing import Tuple
from http import HTTPStatus

from flask import Blueprint, jsonify, request, abort
from flask.wrappers import Response
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError

from app.api.v1.catchers import default_exception_catcher
from app.models import User
from app.extensions import db
from app.exceptions import AlreadyExistsError
from app.schemas import (ProfileSchema,
                         ChangePasswordSchema,
                         UserSchema,
                         ChangeEmailSchema)


my = Blueprint('my', __name__)

profile_schema = ProfileSchema()
password_schema = ChangePasswordSchema()
email_schema = ChangeEmailSchema()


@my.route('/profile', methods=('GET',))
@default_exception_catcher
def get_profile_data() -> Tuple[Response, HTTPStatus]:
    valid_data = profile_schema.load(request.get_json())
    return jsonify(profile_schema.dump(valid_data)), HTTPStatus.OK


@my.route('/change_password', methods=('POST',))
@default_exception_catcher
def change_password() -> Tuple[Response, HTTPStatus]:
    current_user = User.get_by_id('a994dd4c-9836-414c-8b4b-8aef740c11ef')  # mock
    valid_data = password_schema.load(request.get_json())
    if not check_password_hash(current_user.password, valid_data['password']):
        abort(HTTPStatus.UNAUTHORIZED)

    current_user.password = UserSchema.get_password_hash(valid_data['new_password'])
    db.session.commit()
    return jsonify({'message': 'OK'}), HTTPStatus.OK


@my.route('/change_email', methods=('POST',))
@default_exception_catcher
def change_email() -> Tuple[Response, HTTPStatus]:
    current_user = User.get_by_id('a994dd4c-9836-414c-8b4b-8aef740c11ef')  # mock
    valid_data = email_schema.load(request.get_json())
    try:
        current_user.update(valid_data)
    except IntegrityError:
        raise AlreadyExistsError('Адрес электронной почты уже кем-то используется.')
    return jsonify(profile_schema.dump(current_user)), HTTPStatus.OK
