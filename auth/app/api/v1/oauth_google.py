from http import HTTPStatus

from flask import Blueprint, jsonify, request, url_for

from app.api.v1.catchers import default_exception_catcher
from app.schemas import SocialAccountSchema, ProfileSchema
from app.jwt_service import jwt_service
from app.utils import generate_password
from app.pre_configured.oauth import google_client as client
from app.services.sign_in_journal import journal
from app.models import User

google = Blueprint('google', __name__)
social_schema = SocialAccountSchema()
profile_schema = ProfileSchema()


@google.route('/login')
@default_exception_catcher
def login():
    """Google oauth entriepoint"""
    redirect_uri = url_for('google.auth', _external=True)
    return client.authorize_redirect(redirect_uri)


@google.route('/auth')
@default_exception_catcher
def auth():
    """Callback for google oauth. Login or register user."""
    token = client.authorize_access_token()

    user_provider = client.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        token=token
    ).json()
    user_provider['social_name'] = 'google'

    user = User.get_by_email(user_provider['email'])

    if not social_schema.is_account_exists(
        user_provider['id'],
        user_provider['social_name']
    ):
        if not user:
            user = profile_schema.load({
                'email': user_provider['email'],
                'password': generate_password()
            })
            user = user.save()

        social_account = social_schema.load({
            'user_id': user.id,
            'social_id': user_provider['id'],
            'social_name': user_provider['social_name']
        })
        user.social_account.append(social_account)
        user.save()

    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    journal.save_sign_in_entrie(user, request)
    return jsonify({'acsess': access, 'refresh': refresh}), HTTPStatus.OK
