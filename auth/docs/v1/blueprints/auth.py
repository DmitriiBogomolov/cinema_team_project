from flask_restx import Namespace, Resource
from docs.v1.models import limited_user_model, register_model, token_model

namespace = Namespace('Auth',
                      'Основные ручки для аутентификации и авторизации.',
                      path='/')


@namespace.route('/register')
class RegisterHandler(Resource):
    @namespace.response(500, 'Some error.')
    @namespace.expect(register_model, validate=True)
    @namespace.marshal_with(limited_user_model)
    def post(self):
        """Регистрация пользователя"""
        pass


@namespace.route('/login')
class LoginHandler(Resource):
    @namespace.response(500, 'Some error.')
    @namespace.marshal_with(token_model)
    def post(self):
        """Выдает пару токенов в обмен на логин/пароль в basic auth"""
        pass


@namespace.route('/refresh')
class RefreshHandler(Resource):
    @namespace.response(500, 'Some error.')
    @namespace.marshal_with(token_model)
    def post(self):
        """Обновляет пару токенов в обмен на рефреш токен в заголовке"""
        pass


@namespace.route('/logout')
class LogoutHandler(Resource):
    @namespace.response(200, 'Success.')
    @namespace.response(500, 'Some error.')
    def post(self):
        """Отзывает рефреш токен, переданный в заголовке"""
        pass


@namespace.route('/logout_all')
class LogoutAllHandler(Resource):
    @namespace.response(200, 'Success.')
    @namespace.response(500, 'Some error.')
    def post(self):
        """Отзывает все рефреш токены пользователя"""
        pass
