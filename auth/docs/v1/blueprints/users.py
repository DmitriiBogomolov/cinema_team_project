from flask_restx import Namespace, Resource
from docs.v1.models import user_model

namespace = Namespace('Users',
                      'Ручки для работы с пользователями.',
                      path='/api/v1/users')


@namespace.route('')
class UserListHandler(Resource):
    """Получение списка пользователей"""
    @namespace.response(500, 'Some error.')
    @namespace.marshal_list_with(user_model)
    def get(self):
        pass


@namespace.route('/<uuid:user_id>')
class UserHandler(Resource):
    """Чтение, обновление и удаление отдельно указываемого пользователя"""
    @namespace.response(500, 'Some error.')
    @namespace.marshal_with(user_model)
    def get(self, user_id):
        """Получение информации об отдельно указанном пользователе"""
        pass

    @namespace.response(500, 'Some error.')
    @namespace.expect(user_model, validate=True)
    @namespace.marshal_with(user_model)
    def patch(self, user_id):
        """Изменение отдельно указанного пользователя."""
        pass

    @namespace.response(204, 'Success')
    @namespace.response(500, 'Some error.')
    def delete(self, user_id):
        """Удаление отдельно указанного пользователя."""
        pass


@namespace.route('/<uuid:user_id>/roles/<uuid:role_id>')
class RoleHandler(Resource):
    @namespace.response(500, 'Some error.')
    @namespace.marshal_with(user_model, code=200)
    def post(self, user_id, role_id):
        pass

    @namespace.response(204, 'Success')
    @namespace.response(500, 'Some error.')
    def delete(self, user_id, role_id):
        pass
