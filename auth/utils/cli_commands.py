import click
from flask import app
from werkzeug.security import generate_password_hash
from psycopg2 import OperationalError
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.core.extensions import db
from app.services.jwt_service import jwt_service
from app.core.logger import logger
from app.core.config import config


def install_cli_commands(app: app.Flask) -> None:

    @app.cli.command('createsuperuser')
    @click.argument('email')
    @click.argument('password')
    def create_user(email: str, password: str) -> None:
        try:
            password = generate_password_hash(
                password=password,
                method='pbkdf2:sha512',
                salt_length=16
            )
            user = User(
                email=email,
                password=password,
                is_superuser=True
            )

            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print('Already exists')

    @app.cli.command('givemetokens')
    @click.argument('email')
    def get_tokens(email: str) -> None:
        try:
            user = User.get_by_email(email)
            if not user:
                raise OperationalError('No such user')
            access, refresh = jwt_service.create_tokens(user, expires=False)
            jwt_service.save_token(refresh)
            print('Generating access token')
            print(access)
            print('Generating refresh token')
            print(refresh)
        except Exception as e:
            logger.error(e)

    @app.cli.command('load_debug_data')
    def load_debug_data() -> None:
        try:
            password = generate_password_hash(
                password=str(config.debug_user_password),
                method='pbkdf2:sha512',
                salt_length=16
            )
            user = User(
                id='faa01cef-2abb-4e27-a956-9dd313e2cfaf',
                email=str(config.debug_user),
                password=password,
                is_superuser=True
            )

            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print('Already exists')

        print('DEBUG DATA WAS LOADED:')
        print(f'username: {str(config.debug_user)}, password: {str(config.debug_user_password)}')
        print('token:')
        print(str(config.debug_token))
