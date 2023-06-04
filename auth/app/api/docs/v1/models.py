from flask_restx import fields, Model
from flask_restx import Api


id_model_fields = {
    'id': fields.String(
        readonly=True,
        description='UUID',
        pattern='^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    ),
}


timestamped_model_fields = {
    'created': fields.DateTime(
        readonly=True,
        description='Время создания.'
    ),
    'updated': fields.DateTime(
        readonly=True,
        description='Время последнего обновления'
    )
}


role_model = Model('Role', id_model_fields | {
    'name': fields.String(
        required=True,
        description='Название роли'
    ),
    'description': fields.String(
        description='Описание роли.'
    )
} | timestamped_model_fields)


user_model = Model('User', id_model_fields | {
    'email': fields.String(
        required=True,
        description='Эл. почта'
    ),
    'is_active': fields.Boolean(
        description='Указывает на то, что пользователь не заблокирован.'
    ),
    'is_superuser': fields.Boolean(
        readonly=True,
        description='Указывает на суперстатус пользователя.'
    ),
    'roles': fields.Nested(
        role_model,
        readonly=True,
        description='Список ролей',
        as_list=True
    )
} | timestamped_model_fields)


limited_role_model = Model('RoleLimited', id_model_fields | {
    'name': fields.String(
        required=True,
        description='Название роли'
    ),
    'description': fields.String(
        description='Описание роли.'
    )
})


limited_user_model = Model('UserLimited', id_model_fields | {
    'email': fields.String(
        required=True,
        description='Эл. почта'
    ),
    'roles': fields.Nested(
        limited_role_model,
        readonly=True,
        description='Список ролей',
        as_list=True
    )
})


token_model = Model('Token', {
    'access': fields.String(
        required=True,
        description='токен'
    ),
    'refresh': fields.String(
        description='токен'
    )
})


register_model = Model('RegisterModel', {
    'email': fields.String(
        required=True,
        description='Эл. почта'
    ),
    'password': fields.String(
        required=True,
        description='Пароль пользователя.'
    )
})


def register_models(api: Api) -> None:
    api.models[user_model.name] = user_model
    api.models[role_model.name] = role_model
    api.models[limited_user_model.name] = limited_user_model
    api.models[limited_role_model.name] = limited_role_model
    api.models[register_model.name] = register_model
    api.models[token_model.name] = token_model
