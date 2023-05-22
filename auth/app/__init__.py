from flask import Flask

from config import config
from app.extensions import db, ma


def create_app(config=config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    from app.api.swagger import swagger
    from app.api.v1.auth import auth
    from app.api.v1.roles import roles

    app.register_blueprint(auth, url_prefix='/api/v1')
    app.register_blueprint(roles, url_prefix='/api/v1/roles')
    app.register_blueprint(swagger, url_prefix=config.SWAGGER_URL)

    return app
