import falcon
from jwt.exceptions import DecodeError as JWTDecodeError, ExpiredSignatureError
from marshmallow import ValidationError

from yafas.auth.exceptions import JWTInvalidTokenType


def marshmallow_validation_handler(exception, request, response, params):
    response.media = exception.messages
    response.status = falcon.HTTP_400


def unprocessable_entity_handler(exception, request, response, params):
    response.media = {'message': [str(exception)]}
    response.status = falcon.HTTP_422


def unauthorized_handler(exception, request, response, params):
    response.media = {'message': [str(exception)]}
    response.status = falcon.HTTP_401


handlers = [
    (ValidationError, marshmallow_validation_handler),
    (JWTInvalidTokenType, unprocessable_entity_handler),
    (JWTDecodeError, unprocessable_entity_handler),
    (ExpiredSignatureError, unauthorized_handler),
]
