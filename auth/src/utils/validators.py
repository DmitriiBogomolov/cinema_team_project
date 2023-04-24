import string

from marshmallow import validate, ValidationError


def pass_len_validator(value):
    if len(value) < 8:
        raise ValidationError('Must be a minimum eight characters.')


def pass_lowercase_validator(value):
    if not set(value) & set(string.ascii_lowercase):
        raise ValidationError('Must contain a minimum one lowercase letter.')


def pass_uppercase_validator(value):
    if not set(value) & set(string.ascii_uppercase):
        raise ValidationError('Must contain a minimum one uppercase letter.')


def pass_digit_validator(value):
    if not set(value) & set(string.digits):
        raise ValidationError('Must contain a minimum one digit.')


def pass_special_validator(value):
    if not set(value) & set(string.punctuation):
        raise ValidationError('Must contain a minimum one special character.')


password_validator = validate.And(
    pass_len_validator,
    pass_lowercase_validator,
    pass_uppercase_validator,
    pass_digit_validator,
    pass_special_validator
)
