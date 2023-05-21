from flask_swagger_ui import get_swaggerui_blueprint

from settings import app_settings


swagger = get_swaggerui_blueprint(
    app_settings.SWAGGER_URL,
    '/static/docs/openapi.yaml',
    config={
        'app_name': 'Online-cimena auth service'
    }
)
