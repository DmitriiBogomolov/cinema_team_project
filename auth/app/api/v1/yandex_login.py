from http import HTTPStatus

from flask import Blueprint, jsonify, request, url_for

from app.api.v1.catchers import default_exception_catcher
from app.schemas import SocialSchemaYandex, ProfileSchema, SignInEntrieSchema
from app.models import User
from app.jwt_service import jwt_service
from app.utils import generate_password

from app.pre_configured.oauth import yandex

ya = Blueprint('yandex', __name__)
social_schema = SocialSchemaYandex()
profile_schema = ProfileSchema()


@ya.route('/')
def index():
    return '<a href="login">Login with Yandex</a>'


@ya.route('/login')
@default_exception_catcher
def login():
    redirect_uri = url_for('yandex.auth', _external=True)
    return yandex.authorize_redirect(redirect_uri)


@ya.route('/auth')
# @default_exception_catcher
def auth():
    token = yandex.authorize_access_token()
    user_provider = yandex.get('https://login.yandex.ru/info/?format=json', token=token).json()
    user = profile_schema.query_by_email(user_provider)

    if not social_schema.verifi_account(user_provider):
        if not user:
            user = profile_schema.load({
                'email': user_provider['default_email'],
                'password': generate_password()
            })
            id = user.save().id

            social_account = social_schema.load({
                'user_id': id,
                'social_id': user_provider['id'],
                'social_name': 'yandex'
            })
            social_account.save()
        else:
            social_account = social_schema.load({
                'user_id': user.id,
                'social_id': user_provider['id'],
                'social_name': 'yandex'
            })
            social_account.save()

    access, refresh = jwt_service.create_tokens(user)
    jwt_service.save_token(refresh)
    save_signin_entrie(user, request)
    return jsonify({'acsess': access, 'refresh': refresh}), HTTPStatus.OK


def save_signin_entrie(user: User, request: request):
    """Save a record to user log-in history"""
    schema = SignInEntrieSchema()
    entrie = schema.load({
        'user_id': user.id,
        'user_agent': request.user_agent.string,
        'remote_addr': request.environ['REMOTE_ADDR']
    })
    entrie.save()
