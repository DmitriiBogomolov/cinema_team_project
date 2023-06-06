from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
    current_user
)
from functools import wraps
from flask import jsonify


def jwt_roles_required(*roles):
    """Кастомный декоратор для ограничения доступа к ручке на основе данных из токена"""
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            # Проверяем наличие токена
            jwt_identity = get_jwt_identity()
            if not jwt_identity:
                return jsonify({'message': 'Missing Authorization Header'}), 401

            # Получаем данные пользователя
            user_data = get_jwt()['sub']

            # Отдельный секретный обработчик
            if user_data.get('top_secret') and current_user.is_superuser:
                return fn(*args, **kwargs)

            # Проверяем, не заблокирован ли пользователь
            if not user_data.get('is_active'):
                return jsonify({'message': 'The user has been blocked.'}), 403

            # Получаем роли пользователя из токена
            jwt_roles = user_data.get('roles', [])

            # Проверяем наличие в токене одной из допущеных ролей
            if not any(role['name'] in roles for role in jwt_roles):
                return jsonify({'message': 'Insufficient permissions'}), 403

            # Если пользователь имеет необходимые права, то вызываем функцию-обработчик
            return fn(*args, **kwargs)

        return decorator

    return wrapper
