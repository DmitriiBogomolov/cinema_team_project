import os

import yaml
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)


SWAGGER_URL = '/swagger'
API_URL = '/openapi'


@app.route('/openapi')
def openapi():
    with open(os.path.join(os.path.dirname(__file__), 'docs/openapi.yaml')) as f:
        spec = yaml.safe_load(f)
    return spec


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'My API'
    }
)


from src.api.v1.auth import auth


app.register_blueprint(auth, url_prefix='/api/v1')
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run()
