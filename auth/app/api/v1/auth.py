from http import HTTPStatus
import requests

from sqlalchemy.exc import IntegrityError
from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    redirect,
    url_for
)
from flask.wrappers import Response
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    current_user
)
from marshmallow import EXCLUDE

from app.api.v1.catchers import default_exception_catcher
from app.schemas import (
    UserSchema,
    ProfileSchema
)
from app.errors.exceptions import (
    UserAlreadyExists,
    UnavailableRefresh,
)
from app.models import User
from app.services.jwt_service import jwt_service
from app.core.pre_configured.basic_auth import basic_auth
from app.helpers.captcha import handle_captcha
from app.services.sign_in_journal import journal
from app.core.logger import logger
from app.helpers.tokens import generate_token, confirm_token
from app.model_api import ConfirmLetter, RecipientData
from app.core.config import config


auth = Blueprint('auth', __name__)
user_schema = UserSchema()
profile_schema = ProfileSchema()
event_schema = ConfirmLetter()


@auth.route('/register', methods=('GET', 'POST'))
@default_exception_catcher
@handle_captcha
def user_registration() -> tuple[Response, HTTPStatus]:
    if request.method == 'POST':
        data = request.get_json()
        user = profile_schema.load(data, unknown=EXCLUDE)
        try:
            user.save()
        except IntegrityError:
            raise UserAlreadyExists
        else:
            user = user_schema.dump(user)
            token = generate_token(user['email'])
            reference = f'{request.environ["HTTP_ORIGIN"]}/api/v1/confirm_letter/{token}'
            recipient_data = RecipientData(id=user['id'], email=user['email'], message_data=reference)
            event_data = ConfirmLetter(recipient_data=recipient_data)
            try:
                respone = requests.post(config.uri_notification,
                                        headers={'Authorization': config.token_notification,
                                                 'Content-Type': 'application/json',
                                                 'X-Request-Id': request.headers.get('X-Request-Id')},
                                        data=event_data.json()
                                        )

                logger.info(f'{respone.status_code}-{respone.text}')
            except requests.exceptions.ConnectionError:
                redirect(url_for('auth.user_registration'))

        return jsonify(profile_schema.dump(user)), HTTPStatus.CREATED
    return render_template('form_registration.html'), HTTPStatus.OK


@auth.route('/login', methods=('POST', 'GET'))
@basic_auth.login_required
@default_exception_catcher
def login() -> tuple[Response, HTTPStatus]:
    """
    Expected: Basic auth in headers
    """
    user = basic_auth.current_user()
    if user.is_two_auth:
        #  two factor auth handler
        message = request.args
        if message:
            return render_template('form_2F-auth.html', user_id=user.id, message=message['values'])
        return render_template('form_2F-auth.html', user_id=user.id)
    logger.info(request.headers.get('X-Request-Id'))
    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    journal.save_sign_in_entrie(user, request)
    return jsonify({'access': access, 'refresh': refresh}), HTTPStatus.OK


@auth.route('/refresh', methods=('POST',))
@jwt_required(refresh=True)
@default_exception_catcher
def refresh() -> tuple[Response, HTTPStatus]:
    """
    Updates token pair
    Expected: Refresh token in header (Bearer refresh)
    """
    refresh = get_jwt()
    if jwt_service.verify_token(refresh):
        jwt_service.revoke_token(refresh)
        access, refresh = jwt_service.create_tokens(current_user)
        jwt_service.save_token(refresh)

        return jsonify({'access': access, 'refresh': refresh}), HTTPStatus.OK
    raise UnavailableRefresh


@auth.route('/logout', methods=('DELETE',))
@jwt_required(refresh=True)
@default_exception_catcher
def logout() -> tuple[Response, HTTPStatus]:
    """
    Logouts from current device.
    Expected: Refresh token in header (Bearer refresh)
    """
    refresh = get_jwt()
    if jwt_service.verify_token(refresh):
        jwt_service.revoke_token(refresh)
        return jsonify({'message': 'Успешный выход из аккаунта.'}), HTTPStatus.OK
    raise UnavailableRefresh


@auth.route('/logout_all', methods=('DELETE',))
@jwt_required()
@default_exception_catcher
def logout_all() -> tuple[Response, HTTPStatus]:
    """
    Logouts from all devices.
    Expected: Access token in header (Bearer access)
    """
    jwt_service.revoke_user_tokens(User)
    return jsonify({'message': 'Успешный выход из со всех устройств.'}), HTTPStatus.OK


@auth.route('/confirm_letter/<token>', methods=('GET',))
def confirm_letter(token: str):
    email = confirm_token(token)
    user = User.get_by_email(email=email)
    if user.email == email:
        user.update({'is_confirm': True})
    else:
        return jsonify({'message': 'The confirmation link is invalid or has expired.'})
    return jsonify({'message': 'success!'}), HTTPStatus.OK
