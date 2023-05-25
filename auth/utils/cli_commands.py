import click
from flask import app
from psycopg2.errors import UniqueViolation
from werkzeug.security import generate_password_hash

from app.models import User
from app.extensions import db


def install_cli_commands(app: app.Flask) -> None:

    @app.cli.command('createsuperuser')
    @click.argument('email')
    @click.argument('password')
    def create_user(email, password):
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
