from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator


class CategoryValidator(BaseValidator):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
