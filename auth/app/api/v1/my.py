import uuid
from http import HTTPStatus

from flask import Blueprint, jsonify, request, abort
from flask.wrappers import Response
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, current_user

from app.api.v1.catchers import default_exception_catcher
from app.models import AllowedDevice, SignInEntrie
from app.extensions import db
from app.error_handlers.exceptions import UserAlreadyExists
from app.schemas import (ProfileSchema,
                         ChangePasswordSchema,
                         UserSchema,
                         ChangeEmailSchema,
                         AllowedDeviceSchema,
                         SignInEntrieSchema)
from app.helpers import get_pagination_params, get_pagination_meta


my = Blueprint('my', __name__)

profile_schema = ProfileSchema()
password_schema = ChangePasswordSchema()
email_schema = ChangeEmailSchema()
allowed_device_schema = AllowedDeviceSchema()
sign_in_entrie_schema = SignInEntrieSchema()


@my.route('/profile', methods=('GET',))
@jwt_required()
@default_exception_catcher
def get_profile_data() -> tuple[Response, HTTPStatus]:
    """
    Provides current user data.
    """
    return jsonify(profile_schema.dump(current_user)), HTTPStatus.OK


@my.route('/change_password', methods=('POST',))
@jwt_required()
@default_exception_catcher
def change_password() -> tuple[Response, HTTPStatus]:
    """
    Changes current user data.
    Expected: JSON
        "password": "1234567",
        "new_password": "1234567",
        "new_password_re": "1234567"
    """
    valid_data = password_schema.load(request.get_json())
    if not check_password_hash(current_user.password, valid_data['password']):
        abort(HTTPStatus.UNAUTHORIZED)

    current_user.password = UserSchema.get_password_hash(valid_data['new_password'])
    db.session.commit()
    return jsonify({'message': 'OK'}), HTTPStatus.OK


@my.route('/change_email', methods=('POST',))
@jwt_required()
@default_exception_catcher
def change_email() -> tuple[Response, HTTPStatus]:
    """
    Changes current user data.
    Expected: JSON
        "email": "email@inbox.com",
    """
    valid_data = email_schema.load(request.get_json())
    try:
        current_user.update(valid_data)
    except IntegrityError:
        raise UserAlreadyExists
    return jsonify(profile_schema.dump(current_user)), HTTPStatus.OK


@my.route('/history', methods=('GET',))
@jwt_required()
@default_exception_catcher
def sign_in_history() -> tuple[Response, HTTPStatus]:
    """Provides current user sign in journal"""
    page, per_page = get_pagination_params(request)

    entries = (
        SignInEntrie.query
        .filter_by(user_id=current_user.id)
        .order_by(SignInEntrie.created.desc())
        .paginate(page=page, per_page=per_page, error_out=True)
    )
    result = sign_in_entrie_schema.dump(entries, many=True)
    meta = get_pagination_meta(entries)
    return jsonify(data=result, meta=meta), HTTPStatus.OK


@my.route('/allowed_devices', methods=('GET', 'POST'))
@jwt_required()
@default_exception_catcher
def allowed_devices() -> tuple[Response, HTTPStatus]:
    """Provides current user allowed devices"""
    if request.method == 'GET':
        devices = (
            AllowedDevice.query
            .filter_by(user_id=current_user.id)
            .order_by(AllowedDevice.created.desc())
        )
        result = allowed_device_schema.dump(devices, many=True)
        return jsonify(result), HTTPStatus.OK

    elif request.method == 'POST':
        device = allowed_device_schema.load({
            'user_id': current_user.id,
            'user_agent': request.user_agent.string,
        })
        current_user.allowed_devices.append(device)
        db.session.add(device)
        db.session.commit()
        return (
            jsonify(
                allowed_device_schema.dump(
                    current_user.allowed_devices,
                    many=True
                )
            ),
            HTTPStatus.CREATED
        )


@my.route('/allowed_devices/<uuid:id>/', methods=('DELETE',))
@jwt_required()
@default_exception_catcher
def delete_allowed_device(id: uuid.UUID) -> tuple[Response, HTTPStatus]:
    """Deletes allowed device"""
    device = AllowedDevice.get_by_id(id)

    device.delete()

    return (
        jsonify(
            allowed_device_schema.dump(
                current_user.allowed_devices,
                many=True
            )
        ),
        HTTPStatus.OK
    )
