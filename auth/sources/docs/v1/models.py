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


profile_role_model = Model('Role', id_model_fields | {
    'name': fields.String(
        required=True,
        description='Название роли'
    ),
    'description': fields.String(
        description='Описание роли.'
    )
})


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


profile_model = Model('Profile', id_model_fields | {
    'email': fields.String(
        required=True,
        description='Эл. почта'
    ),
    'is_active': fields.Boolean(
        description='Указывает на то, что пользователь не заблокирован.'
    ),
    'roles': fields.Nested(
        profile_role_model,
        readonly=True,
        description='Список ролей',
        as_list=True
    )
})


change_password_model = Model('ChangePassword', {
    'password': fields.String(
        required=True,
        description='Текущий пользователя.'
    ),
    'new_password': fields.String(
        required=True,
        description='Новый пароль.'
    ),
    'new_password_re': fields.String(
        required=True,
        description='Новый пароль повторно'
    )
})

change_email_model = Model('ChangeEmail', {
    'email': fields.String(
        required=True,
        description='Эл. почта'
    )
})

entrie_record_model = Model('EntrieRecord', id_model_fields | {
    'remote_addr': fields.String(
        required=True,
        description='IP адрес, с коротрого совершался вход'
    ),
    'user_agent': fields.String(
        required=True,
        description='Устройство, с коротрого совершался вход'
    ),
    'user_id': fields.String(
        required=True,
        description='UUID пользовтеля',
        pattern='^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    )
})


pagination_meta_model = Model('Pagination', {
    'has_next': fields.Boolean(
        required=True,
        description='Указывает, есть ли следующая страница.'
    ),
    'has_prev': fields.Boolean(
        required=True,
        description='Указывает, есть ли предыдущая страница.'
    ),
    'next_page': fields.Boolean(
        required=True,
        description='Следующая страница.'
    ),
    'page': fields.Integer(
        required=True,
        description='Номер страницы.'
    ),
    'pages': fields.Integer(
        required=True,
        description='Всего страниц.'
    ),
    'prev_page': fields.Integer(
        required=True,
        description='Предыдущая страница.'
    ),
    'total_count': fields.Integer(
        required=True,
        description='Всего записей.'
    )
})


entrie_joural_model = Model('EntrieJournal', {
    'data': fields.Nested(
        entrie_record_model,
        readonly=True,
        description='Список входов в систему.',
        as_list=True
    ),
    'meta': fields.Nested(
        pagination_meta_model,
        readonly=True,
        description='Метаданные пагинации',
    )
})


allowed_device_model = Model('Allowed_device', id_model_fields | {
    'user_agent': fields.String(
        required=True,
        description='Разрешенное устройство'
    ),
    'user_id': fields.String(
        required=True,
        description='UUID пользовтеля',
        pattern='^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    )
})


def load_models(api: Api) -> None:
    api.models[user_model.name] = user_model
    api.models[role_model.name] = role_model
    api.models[limited_user_model.name] = limited_user_model
    api.models[limited_role_model.name] = limited_role_model
    api.models[register_model.name] = register_model
    api.models[token_model.name] = token_model
    api.models[profile_model.name] = profile_model
    api.models[profile_role_model.name] = profile_role_model
    api.models[change_password_model.name] = change_password_model
    api.models[change_email_model.name] = change_email_model
    api.models[entrie_record_model.name] = entrie_record_model
    api.models[pagination_meta_model.name] = pagination_meta_model
    api.models[entrie_joural_model.name] = entrie_joural_model
    api.models[allowed_device_model.name] = allowed_device_model
