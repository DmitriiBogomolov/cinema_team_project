import click
from flask import app
from sqlalchemy.exc import IntegrityError

from src.models import db, User, Role


def install_cli_commands(app: app.Flask) -> None:

    @app.cli.command('createsuperuser')
    @click.argument('name')
    @click.argument('password')
    def create_user(name, password):
        try:
            role = Role.query.filter_by(name='superuser').first() \
                or Role(name='superuser')
            user = User(email=name, password=password)
            user.roles.append(role)

            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(e)
