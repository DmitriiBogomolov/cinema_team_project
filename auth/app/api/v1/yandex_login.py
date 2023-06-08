from http import HTTPStatus

from flask import Blueprint, jsonify, request, url_for

from app.api.v1.catchers import default_exception_catcher
from app.schemas import SocialAccountSchema, ProfileSchema
from app.jwt_service import jwt_service
from app.utils import generate_password
from app.api.v1.save_history import save_signin_entrie
from app.pre_configured.oauth import yandex

ya = Blueprint('yandex', __name__)
social_schema = SocialAccountSchema()
profile_schema = ProfileSchema()


@ya.route('/login')
@default_exception_catcher
def login():
    redirect_uri = url_for('yandex.auth', _external=True)
    return yandex.authorize_redirect(redirect_uri)


@ya.route('/auth')
@default_exception_catcher
def auth():
    token = yandex.authorize_access_token()

    user_provider = yandex.get('https://login.yandex.ru/info', token=token).json()
    user_provider['social_name'] = 'yandex'

    user = profile_schema.get_by_email(user_provider['default_email'])

    if not social_schema.verifi_account(
        user_provider['id'],
        user_provider['social_name']
    ):
        if not user:
            # save in the users table
            user = profile_schema.load({
                'email': user_provider['default_email'],
                'password': generate_password()
            })
            user = user.save()

        # save in the social_account table
        social_account = social_schema.load({
            'user_id': user.id,
            'social_id': user_provider['id'],
            'social_name': user_provider['social_name']
        })
        social_account.save()

    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    save_signin_entrie(user, request)
    return jsonify({'acsess': access, 'refresh': refresh}), HTTPStatus.OK
