from marshmallow import Schema, ValidationError, fields, post_load, validates

from yafas import db
from yafas.auth.models import User

from .models import BetaUser


class RegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @validates('email')
    def validate_email_is_free(self, value) -> bool:
        if User.query.filter_by(email=value).first():
            raise ValidationError('This email is already in use.')
        return True

    @post_load
    def create_beta_user(self, data) -> BetaUser:
        beta = BetaUser(**data)
        db.session.add(beta)
        db.session.commit()
        return beta
