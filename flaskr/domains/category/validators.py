from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator


class CategoryCreateValidator(BaseValidator):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))


class CategoryUpdateValidator(BaseValidator):
    name = fields.Str(validate=validate.Length(min=3, max=50))
