import falcon
from marshmallow import ValidationError


def marshmallow_validation_handler(exception, request, response, params):
    response.media = exception.messages
    response.status = falcon.HTTP_400


handlers = [
    (ValidationError, marshmallow_validation_handler),
]
