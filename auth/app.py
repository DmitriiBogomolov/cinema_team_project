import os
from datetime import timedelta

import redis
import yaml
from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from utils.cli_commands import install_cli_commands
from settings import app_settings
from src.pre_configured.jwt import get_jwt_manager
from src.pre_configured.basic_auth import get_basic_auth
from src.error_handlers import register_error_handlers
from src.models import db

app = Flask(__name__)

ACCESS_EXP = timedelta(seconds=app_settings.JWT_ACCESS_TOKEN_EXPIRES)
REFRESH_EXP = timedelta(seconds=app_settings.JWT_REFRESH_TOKEN_EXPIRES)

SWAGGER_URL = '/swagger'
API_URL = '/openapi'


@app.route('/openapi')
def openapi():
    with open(os.path.join(os.path.dirname(__file__), 'docs/openapi.yaml')) as f:
        spec = yaml.safe_load(f)
    return spec


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My API'
    }
)

cors = CORS(app, resources={r'/api/*': {'origins': '*'}})  # разрешаем CORS для работы фронтенда
app.config['JWT_SECRET_KEY'] = app_settings.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXP
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXP
app.config['SQLALCHEMY_DATABASE_URI'] = app_settings.POSTGRES_DSN


db.init_app(app)
migrate = Migrate(app, db)

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
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


register_error_handlers(app)
install_cli_commands(app)
