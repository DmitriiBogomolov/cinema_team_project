from flask import Flask

from utils.cli_commands import install_cli_commands
from config import config
from app.extensions import db, ma, migrate
from app.pre_configured.jwt_manager import init_jwt_manager
from app.error_handlers import register_error_handlers
from app.pre_configured.oauth import oauth
from middlewares.token_bucket import token_bucket_middleware


def create_app(config=config):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'random-secret-key'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 15 * 60  # 15 minutes
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 14 * (24 * 60 * 60)  # 14 days
    app.config['REFRESH_TOKEN_EXP'] = config.refresh_token_exp
    app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri

    init_jwt_manager(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    oauth.init_app(app)

    from docs.v1 import docs
    from app.api.v1.auth import auth
    from app.api.v1.roles import roles
    from app.api.v1.users import users
    from app.api.v1.my import my
    from app.api.v1.captcha import captcha
    from app.api.v1.yandex_login import ya
    from app.api.v1.auth_2f import auth_2f

    app.register_blueprint(captcha, url_prefix='/captcha')
    app.register_blueprint(auth, url_prefix='/api/v1')
    app.register_blueprint(auth_2f, url_prefix='/api/v1')
    app.register_blueprint(roles, url_prefix='/api/v1/roles')
    app.register_blueprint(users, url_prefix='/api/v1/users')
    app.register_blueprint(my, url_prefix='/api/v1/my')
    app.register_blueprint(ya, url_prefix='/api/v1/yandex')
    app.register_blueprint(docs, url_prefix=config.swagger_url)

    install_cli_commands(app)
    register_error_handlers(app)

    if not config.debug:
        app.wsgi_app = token_bucket_middleware(app.wsgi_app)

    return app
