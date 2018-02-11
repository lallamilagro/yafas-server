import falcon

from . import schemas
from .models import User

# @jwt.invalid_token_loader
# def invalid_token(reason):
#     return {'message': [reason]}, 422


# @jwt.expired_token_loader
# def token_expired():
#     return {'message': ['Token has expired.']}, 401

class CheckEmail:
    def on_get(self, request, response, email):
        schemas.EmailSchema(strict=True).load({'email': email})
        response.media = {}


def login():
    tokens, errors = schemas.LoginSchema().load(request.json)
    return (errors, 400) if errors else (tokens, 201)


class Register:
    def on_post(self, request, response):
        schemas.RegistrationSchema(strict=True).load(request.media)
        response.media = {}
        response.status = falcon.HTTP_201


def refresh():
    user = User.jwt_retrieve()
    return {
        'access_token': user.create_access_token(),
        'refresh_token': user.create_refresh_token(),
    }, 201
