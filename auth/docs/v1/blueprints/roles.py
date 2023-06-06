from flask_restx import Namespace, Resource
from docs.v1.models import role_model

namespace = Namespace('Roles',
                      'Ручки для работы с ролями.',
                      path='/api/v1/roles')


@namespace.route('')
class RolesHandler(Resource):
    """Получение списка ролей"""
    @namespace.response(500, 'Some error.')
    @namespace.marshal_list_with(role_model)
    def get(self):
        pass


@namespace.route('/<uuid:role_id>')
class CurrentRoleHandler(Resource):
    """Чтение, обновление и удаление отдельно указанных ролей"""
    @namespace.response(500, 'Some error.')
    @namespace.marshal_with(role_model)
    def get(self, role_id):
        """Получение информации об отдельно указанной роли."""
        pass

    @namespace.response(500, 'Some error.')
    @namespace.expect(role_model, validate=True)
    @namespace.marshal_with(role_model)
    def patch(self, role_id):
        """Изменение отдельно указанной роли."""
        pass

    @namespace.response(204, 'Success')
    @namespace.response(500, 'Some error.')
    def delete(self, role_id):
        """Удаление отдельно указанной роли."""
        pass
