from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator


class TableCreateValidator(BaseValidator):
    name = fields.Str(validate=[validate.Length(min=3, max=30)])


class TableUpdateValidator(BaseValidator):
    name = fields.Str(validate=[validate.Length(min=3, max=30)])
