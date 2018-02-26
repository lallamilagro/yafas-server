from marshmallow import Schema, ValidationError, fields, post_load, validates

from yafas import db
from yafas.base import StrictSchema

from .models import User


class EmailSchema(StrictSchema):
    email = fields.Email(required=True)

    @validates('email')
    def validate_email_is_free(self, value) -> bool:
        if User.query.filter_by(email=value).first():
            raise ValidationError('This email is already in use.')
        return True


class RegistrationSchema(EmailSchema):
    password = fields.Str(required=True)

    @post_load
    def create_user(self, data) -> str:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user.create_access_token()


class LoginSchema(StrictSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @post_load
    def create_tokens(self, data) -> str:
        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            raise ValidationError('Not a valid credentials.', 'message')

        return user.create_access_token()


class UserInfoSchema(Schema):
    email = fields.Email(required=True)
    id = fields.Int(required=True)
    registered_in = fields.DateTime(required=True)
