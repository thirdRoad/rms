from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator


class ProductCreateValidator(BaseValidator):
    name = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    stock = fields.Int(required=True, validate=validate.Range(min=0))
    category_id = fields.Int(required=True, validate=validate.Range(min=1))


class ProductUpdateValidator(BaseValidator):
    name = fields.Str(validate=validate.Length(min=3, max=50))
    price = fields.Float(validate=validate.Range(min=0))
    stock = fields.Int(validate=validate.Range(min=0))
    category_id = fields.Int(validate=validate.Range(min=1))
