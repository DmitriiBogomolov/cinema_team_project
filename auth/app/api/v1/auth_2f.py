from http import HTTPStatus

import pyotp
from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    redirect,
    url_for
)
from flask.wrappers import Response

from app.api.v1.catchers import default_exception_catcher
from app.schemas import AddOtpSecretSchema

from app.models import User
from app.services.jwt_service import jwt_service
from app.core.pre_configured.basic_auth import basic_auth
from app.services.sign_in_journal import journal


auth_2f = Blueprint('auth_2f', __name__)
otp_secret_shema = AddOtpSecretSchema()


@auth_2f.route('/sync', methods=('GET',))
@basic_auth.login_required
@default_exception_catcher
def sync() -> tuple[Response, HTTPStatus]:
    """Enable TOTP two factor for current user"""
    user = basic_auth.current_user()
    otp_secret = pyotp.random_base32()
    otp_secret_user = otp_secret_shema.load(
        {'otp_secret': otp_secret}
    )

    user.update(otp_secret_user)
    totp = pyotp.TOTP(otp_secret)
    otp_url = totp.provisioning_uri(
        name=f'{user.id}@manyfilms.ru',
        issuer_name='2FA-DEMO'
    )
    message = request.args
    if message:
        #  при ошибочном вводе кода из TOTP приложения
        return render_template(
            'register_2F-auth.html',
            otp_url=otp_url,
            user_id=user.id,
            message=message['values']
        ), HTTPStatus.OK
    #  при успешной синхронизации
    return render_template(
        'register_2F-auth.html',
        otp_url=otp_url,
        user_id=user.id,
        message=''
    ), HTTPStatus.OK


@auth_2f.route('/sync_check/<user_id>', methods=('POST',))
@default_exception_catcher
def sync_check(user_id: str) -> tuple[Response, HTTPStatus]:
    """Checks the TOTP code from sync form"""
    user = User.get_by_id(user_id)
    totp = pyotp.TOTP(user.otp_secret)

    if not totp.verify(request.form['code']):
        return redirect(
            url_for('auth_2f.sync', values='invalid code')
        ), HTTPStatus.FOUND

    otp_secret_user = otp_secret_shema.load({'is_two_auth': True})
    user.update(otp_secret_user)
    return jsonify(
        'two-factor authorization is enabled'
    ), HTTPStatus.OK


@auth_2f.route('/check_verify/<user_id>', methods=('POST', 'GET'))
@default_exception_catcher
def check_verify(user_id: str) -> tuple[Response, HTTPStatus]:
    """Checks the TOTP code from login form"""
    user = User.get_by_id(user_id)
    totp = pyotp.TOTP(user.otp_secret)

    if not totp.verify(request.form['code']):
        return redirect(
            url_for('auth.login', values='invalid code')
        ), HTTPStatus.FOUND

    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    journal.save_sign_in_entrie(user, request)
    return jsonify(
        {'access': access, 'refresh': refresh}
    ), HTTPStatus.OK
