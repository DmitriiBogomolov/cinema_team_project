import click
from flask import app
from psycopg2.errors import UniqueViolation
from werkzeug.security import generate_password_hash
from psycopg2 import OperationalError

from app.models import User
from app.extensions import db
from app.jwt_service import jwt_service
from logger import logger


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
        except UniqueViolation as e:
            db.session.rollback()
            print(e)

    @app.cli.command('givemetokens')
    @click.argument('email')
    def get_tokens(email: str) -> None:
        try:
            user = User.get_by_email(email)
            if not user:
                raise OperationalError('No such user')
            access, refresh = jwt_service.create_tokens(user, expires=False)
            jwt_service.save_token(refresh)
            logger.info('Generating access token')
            print(access)
            logger.info('Generating refresh token')
            print(refresh)
        except Exception as e:
            logger.error(e)
