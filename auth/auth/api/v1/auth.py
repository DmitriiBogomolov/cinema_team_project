from flask import Blueprint, request, json

from auth.db.postgres import db
from auth.schemas import UserSchema


auth = Blueprint('auth', __name__)


@auth.route('/hello-world')
def hello_world():
    return 'Hello, World!'


@auth.route('/register', methods=('POST',))
def register():
    json_data = json.loads(request.data)
    user_schema = UserSchema()

    user = user_schema.load(json_data)

    db.session.add(user)
    db.session.commit()
