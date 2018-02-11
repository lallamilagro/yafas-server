from marshmallow import ValidationError, fields, post_load, validates

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
    def create_user(self, data) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {
            'access_token': user.create_access_token(),
            'refresh_token': user.create_refresh_token(),
        }


class LoginSchema(StrictSchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

    @post_load
    def create_tokens(self, data) -> tuple:
        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            raise ValidationError('Not a valid credentials.', 'message')

        return {
            'access_token': user.create_access_token(),
            'refresh_token': user.create_refresh_token(),
        }
