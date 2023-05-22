from flask_swagger_ui import get_swaggerui_blueprint

from config import config


swagger = get_swaggerui_blueprint(
    config.SWAGGER_URL,
    '/static/openapi.yaml',
    config={
        'app_name': 'Online-cimena auth service'
    }
)
