import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from app.core.config import config


def init_sdk_service():
    sentry_sdk.init(
        dsn=config.dsn,
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0
    )
