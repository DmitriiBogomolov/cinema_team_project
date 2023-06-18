from http import HTTPStatus

from flask import Blueprint, jsonify, request, url_for

from app.api.v1.catchers import default_exception_catcher
from app.schemas import SocialAccountSchema, ProfileSchema
from app.services.jwt_service import jwt_service
from app.helpers.passwords import generate_password
from app.services.sign_in_journal import journal
from app.models import User
from app.core.pre_configured.oauth import providers

open_auth = Blueprint('open_auth', __name__)
social_schema = SocialAccountSchema()
profile_schema = ProfileSchema()


@open_auth.route('/login')
@default_exception_catcher
def login():
    """Oauth entriepoint"""
    provider = providers.get(request.args.get('provider'))
    redirect_uri = '{}?provider={}'.format(
        url_for('open_auth.callback', _external=True),
        provider.name
    )
    return provider.client.authorize_redirect(redirect_uri)


@open_auth.route('/callback')
@default_exception_catcher
def callback():
    """Callback for provider oauth. Login or register user."""
    provider = providers.get(request.args.get('provider'))
    user_data = provider.get_user_info()

    user = User.get_by_email(user_data['email'])

    if not social_schema.is_account_exists(
        user_data['id'],
        provider.name
    ):
        if not user:
            user = profile_schema.load({
                'email': user_data['email'],
                'password': generate_password()
            })
            user = user.save()

        social_account = social_schema.load({
            'user_id': user.id,
            'social_id': user_data['id'],
            'social_name': provider.name
        })
        user.social_account.append(social_account)
        user.save()

    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    journal.save_sign_in_entrie(user, request)
    return jsonify({'acsess': access, 'refresh': refresh}), HTTPStatus.OK
