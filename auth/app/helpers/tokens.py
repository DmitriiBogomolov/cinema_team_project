from itsdangerous import URLSafeTimedSerializer
from app.core.config import config


def generate_token(email):
    serializer = URLSafeTimedSerializer(config.secret_key)
    return serializer.dumps(email, salt=config.security_password_salt)


def confirm_token(token, expiration=360):
    serializer = URLSafeTimedSerializer(config.secret_key)
    try:
        email = serializer.loads(
            token, salt=config.security_password_salt, max_age=expiration
        )
        return email
    except Exception:
        return False
