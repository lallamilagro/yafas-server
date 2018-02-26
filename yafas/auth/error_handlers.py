import falcon
from jwt.exceptions import DecodeError as JWTDecodeError, ExpiredSignatureError

from .exceptions import JWTNoTokens


def unprocessable_entity_handler(exception, request, response, params):
    response.media = {'message': [str(exception)]}
    response.status = falcon.HTTP_422


def unauthorized_handler(exception, request, response, params):
    response.media = {'message': [str(exception)]}
    response.status = falcon.HTTP_401


handlers = (
    (JWTNoTokens, unauthorized_handler),
    (JWTDecodeError, unprocessable_entity_handler),
    (ExpiredSignatureError, unauthorized_handler),
)
