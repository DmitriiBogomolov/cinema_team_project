from datetime import timedelta

import redis
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from settings import app_settings
from src.pre_configured.jwt import get_jwt_manager
from src.pre_configured.basic_auth import get_basic_auth
from src.models import db


ACCESS_EXP = timedelta(seconds=app_settings.JWT_ACCESS_TOKEN_EXPIRES)
REFRESH_EXP = timedelta(seconds=app_settings.JWT_REFRESH_TOKEN_EXPIRES)


app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})  # разрешаем CORS для работы фронтенда
app.config['JWT_SECRET_KEY'] = app_settings.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXP
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXP
app.config['SQLALCHEMY_DATABASE_URI'] = app_settings.POSTGRES_DSN


db.init_app(app)

ma = Marshmallow(app)
jwt = get_jwt_manager(app)
basic_auth = get_basic_auth()

refresh_blacklist = redis.StrictRedis(
    host=app_settings.REDIS_HOST,
    port=app_settings.REDIS_PORT,
    db=0
)

from src.api.v1.auth import auth
from src.api.v1.users import users
from src.api.v1.roles import roles


app.register_blueprint(auth, url_prefix='/api/v1')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(roles, url_prefix='/api/v1/roles')


with app.app_context():
    db.create_all()
