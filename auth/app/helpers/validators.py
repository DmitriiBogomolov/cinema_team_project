import string

from marshmallow import validate, ValidationError


def min_len_validator(value: str) -> None:
    if len(value) < 8:
        raise ValidationError('Must be a minimum eight characters.')


def has_lowercase_validator(value: str) -> None:
    if not set(value) & set(string.ascii_lowercase):
        raise ValidationError('Must contain a minimum one lowercase letter.')


def has_uppercase_validator(value: str) -> None:
    if not set(value) & set(string.ascii_uppercase):
        raise ValidationError('Must contain a minimum one uppercase letter.')


def has_digit_validator(value: str) -> None:
    if not set(value) & set(string.digits):
        raise ValidationError('Must contain a minimum one digit.')


def has_special_validator(value: str) -> None:
    if not set(value) & set(string.punctuation):
        raise ValidationError('Must contain a minimum one special character.')


password_validator = validate.And(
    min_len_validator,
)
