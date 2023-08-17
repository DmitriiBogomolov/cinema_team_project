from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

from utils.cli_commands import install_cli_commands
from app.core.config import config
from app.core.extensions import db, ma, migrate
from app.core.pre_configured.jwt_manager import init_jwt_manager
from app.errors import register_error_handlers
from app.core.pre_configured.oauth import oauth
from middlewares.token_bucket import token_bucket_middleware
from middlewares.set_header_request_id import init_header_request_id
from app.services.sdk_servise import init_sdk_service


def configure_tracer() -> None:
    resource = Resource(attributes={
        'service.name': 'auth'
    })
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=config.jaeger_host,
                agent_port=config.jaeger_port,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    if config.print_traces:
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )


def create_app(config=config):
    if config.enable_tracer:
        configure_tracer()

    init_sdk_service()

    app = Flask(__name__)
    FlaskInstrumentor().instrument_app(app)
    init_header_request_id(app)

    app.config['SERVER_NAME'] = config.server_name
    app.config['SECRET_KEY'] = config.secret_key
    app.config['JWT_SECRET_KEY'] = config.jwt_secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 15 * 60  # 15 minutes
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 14 * (24 * 60 * 60)  # 14 days
    app.config['REFRESH_TOKEN_EXP'] = config.refresh_token_exp
    app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
    app.config['SECURITY_PASSWORD_SALT'] = config.security_password_salt

    init_jwt_manager(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    oauth.init_app(app)

    from sources.docs.v1 import docs
    from app.api.v1.auth import auth
    from app.api.v1.two_factor import two_factor
    from app.api.v1.roles import roles
    from app.api.v1.users import users
    from app.api.v1.my import my
    from app.api.v1.captcha import captcha
    from app.api.v1.open_auth import open_auth
    from app.api.v1.service import service

    app.register_blueprint(captcha, url_prefix='/captcha')
    app.register_blueprint(auth, url_prefix='/api/v1')
    app.register_blueprint(two_factor, url_prefix='/api/v1')
    app.register_blueprint(roles, url_prefix='/api/v1/roles')
    app.register_blueprint(users, url_prefix='/api/v1/users')
    app.register_blueprint(my, url_prefix='/api/v1/my')
    app.register_blueprint(open_auth, url_prefix='/api/v1/oauth')
    app.register_blueprint(docs, url_prefix='/swagger')
    app.register_blueprint(service, url_prefix='/api/v1/service')

    install_cli_commands(app)
    register_error_handlers(app)

    if not config.debug:
        app.wsgi_app = token_bucket_middleware(app.wsgi_app)

    return app
