from auth import ma
from auth.models import User

from marshmallow import fields, validate, post_load
from werkzeug.security import generate_password_hash


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    email = fields.Email(required=True)

    password = fields.String(
        required=True,
        validate=validate.Regexp(
            '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,32}$',
            error='Password is too simple. Must be a minimum eight characters, '
                  'at least one uppercase letter, one lowercase letter, one number and one special character.'
        )
    )

    @post_load
    def make_obj(self, data, **kwargs):
        data['password'] = generate_password_hash(data['password'])
        return User(**data)
