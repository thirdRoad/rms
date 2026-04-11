from marshmallow import fields, validate

from flaskr.core.base.validators import BaseValidator
from flaskr.domains.tables.models import TableStatus


class TableUpdateValidator(BaseValidator):
    status = fields.Str(
        required=True,
        validate=validate.OneOf([s.value for s in TableStatus]),
    )
