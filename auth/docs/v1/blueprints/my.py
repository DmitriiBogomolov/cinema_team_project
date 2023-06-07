from flask_restx import Namespace, Resource
from docs.v1.models import (
    profile_model,
    change_email_model,
    change_password_model,
    entrie_joural_model,
    allowed_device_model
)

namespace = Namespace('My',
                      'Ручки для работы с текущим пользователем.',
                      path='/api/v1/my')


@namespace.route('/profile')
class UserHandler(Resource):
    """Просмотр профиля текущего пользователя"""
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    @namespace.marshal_with(profile_model)
    def get(self):
        pass


@namespace.route('/change_password')
class ChangePasswordHandler(Resource):
    """Изменение пароля текущего пользователя"""
    @namespace.response(200, 'Success.')
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    @namespace.expect(change_password_model, validate=True)
    def post(self):
        pass


@namespace.route('/change_email')
class ChangeEmailHandler(Resource):
    """Изменение емейла текущего пользователя"""
    @namespace.response(200, 'Success.')
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    @namespace.expect(change_email_model, validate=True)
    def post(self):
        pass


@namespace.route('/history')
class HistoryHandler(Resource):
    """История входов в аккаунт"""
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    @namespace.marshal_with(entrie_joural_model)
    def get(self):
        pass


@namespace.route('/allowed_devices')
class AllowedDeviceListHandler(Resource):
    """Получение списка разрешенных устройств"""
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    @namespace.marshal_list_with(allowed_device_model)
    def get(self):
        pass


@namespace.route('/allowed_devices/<uuid:device_id>')
class AllowedDevicHandler(Resource):
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    @namespace.marshal_list_with(allowed_device_model)
    def post(self, user_id, role_id):
        pass

    @namespace.response(204, 'Success')
    @namespace.response(500, 'Some error.')
    @namespace.doc(security='JWTAuth')
    def delete(self, user_id, role_id):
        pass
