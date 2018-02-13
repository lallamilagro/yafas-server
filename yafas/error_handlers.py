import falcon
from marshmallow import ValidationError

from yafas.auth.error_handlers import handlers as auth_error_handlers


def marshmallow_validation_handler(exception, request, response, params):
    response.media = exception.messages
    response.status = falcon.HTTP_400


handlers = (
    (ValidationError, marshmallow_validation_handler),
    *auth_error_handlers,
)
