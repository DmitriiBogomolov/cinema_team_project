import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


def init_sdk_service():
    sentry_sdk.init(
        dsn='https://e91f901f7316439ea928ff90dec00904@o4505504683655168.ingest.sentry.io/4505562211221504',
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0
    )
