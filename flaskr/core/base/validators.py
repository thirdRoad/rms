from marshmallow import Schema, ValidationError


class BaseValidator(Schema):
    def validate_data(self, data: dict) -> dict:
        errors = self.validate(data)
        if errors:
            raise ValidationError(errors)
        return self.load(data)
