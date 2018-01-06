from marshmallow import Schema, ValidationError, fields, validates

from .models import User


class EmailSchema(Schema):
    email = fields.Email(required=True)

    @validates('email')
    def validate_email_is_free(self, value) -> bool:
        if User.query.filter_by(email=value).first():
            raise ValidationError('This email is already in use.')
        return True
