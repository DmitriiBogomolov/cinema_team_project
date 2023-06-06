from flask import Blueprint
from flask_restx import Api
from docs.v1.blueprints.auth import namespace as auth
from docs.v1.blueprints.users import namespace as users
from docs.v1.blueprints.roles import namespace as roles
from docs.v1.blueprints.my import namespace as my
from docs.v1.models import load_models

docs = Blueprint('swagger', __name__)

api_extension = Api(
    docs,
    title='Сервис аутентификации онлайн-кинотеатра',
    version='1.0',
    description='Используемые технологии:'
                '<ul><li>flask;</li>'
                '<li>SQLAlchemy в качестве ORM;</li>'
                '<li>marshmallow для валидации и сериализации;</li>'
                '<li>храним Json Web Tokens в Redis;</li>'
                '<li>ролевая модель разграничения доступов.</li></ul>',
    doc='/doc',
)

load_models(api_extension)

api_extension.add_namespace(auth)
api_extension.add_namespace(my)
api_extension.add_namespace(users)
api_extension.add_namespace(roles)
