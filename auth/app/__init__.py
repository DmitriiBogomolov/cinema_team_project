from flask import Flask

from config import config
from app.extensions import db, ma


def create_app(config=config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)

    from app.api.swagger import swagger
    from app.api.v1.auth import auth
    from app.api.v1.roles import roles
    from app.api.v1.users import users

    app.register_blueprint(auth, url_prefix='/api/v1')
    app.register_blueprint(roles, url_prefix='/api/v1/roles')
    app.register_blueprint(users, url_prefix='/api/v1/users')
    app.register_blueprint(swagger, url_prefix=config.SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app
