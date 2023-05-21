from flask import Flask

from settings import app_settings
from src.models import db


app = Flask(__name__, static_url_path='/static')


app.config['SQLALCHEMY_DATABASE_URI'] = app_settings.POSTGRES_DSN

db.init_app(app)

with app.app_context():
    db.create_all()


from src.api.swagger import swagger
from src.api.v1.auth import auth


app.register_blueprint(auth, url_prefix='/api/v1')
app.register_blueprint(swagger, url_prefix=app_settings.SWAGGER_URL)


if __name__ == '__main__':
    app.run()
