from werkzeug.exceptions import Unauthorized
from werkzeug.exceptions import NotFound


class BaseError(Exception):
    """Provided base exception for endpoint handlers"""
    default_message = 'Something went wrong (custom).'

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)


class CaptchaError(BaseError):
    pass


class NoCaptchaError(CaptchaError):
    default_message = 'Captcha is required'


class WrongCaptchaError(CaptchaError):
    default_message = 'Wrong captcha provided.'


class NotFoundError(BaseError, NotFound):
    """Raises if some entity not found"""
    default_message = 'Requested resource not found.'


class BaseAlreadyExists(BaseError):
    """Base exception if some entity already exist"""
    default_message = 'This entity already exists.'


class UserAlreadyExists(BaseAlreadyExists):
    """Raises if user exist"""
    default_message = 'The email address is already in use.'


class BaseUnauthorized(BaseError, Unauthorized):
    """Base exception if user unauthorized"""
    default_message = 'Unauthorized or wrong user credentials.'


class UnavailableRefresh(BaseUnauthorized):
    """Raises if:"""
    default_message = 'This token has already been used before.'
