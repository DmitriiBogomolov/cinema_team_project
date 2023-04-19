from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from auth.settings import app_settings


db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = app_settings.POSTGRES_DSN
    db.init_app(app)
