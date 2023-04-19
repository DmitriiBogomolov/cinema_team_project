from flask import Flask
from flask_marshmallow import Marshmallow

from auth.db.postgres import init_db


app = Flask(__name__)

init_db(app)
ma = Marshmallow(app)


from auth.api.v1.auth import auth
from auth.api.v1.users import users
from auth.api.v1.roles import roles

app.register_blueprint(auth, url_prefix='/api/v1')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(roles, url_prefix='/api/v1/roles')
