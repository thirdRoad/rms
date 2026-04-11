from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator


class AuthLoginValidator(BaseValidator):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    password = fields.Str(required=True, validate=validate.Length(min=6, max=128))
