from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator


class UserCreateValidator(BaseValidator):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
    display_name = fields.Str(required=True, validate=validate.Length(min=3, max=16))
    email = fields.Email(required=True)
    role_id = fields.Int(required=True)


class UserUpdateValidator(BaseValidator):
    username = fields.Str(validate=validate.Length(min=3, max=32))
    password = fields.Str(validate=validate.Length(min=6, max=128))
    display_name = fields.Str(validate=validate.Length(min=3, max=16))
    email = fields.Email()
    role_id = fields.Int()
