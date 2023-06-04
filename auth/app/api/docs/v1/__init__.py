from flask import Blueprint
from flask_restx import Api
from app.api.docs.v1.blueprints.auth import namespace as auth
from app.api.docs.v1.blueprints.users import namespace as users
from app.api.docs.v1.models import register_models

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

register_models(api_extension)


api_extension.add_namespace(auth)
api_extension.add_namespace(users)
