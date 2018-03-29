import falcon
from marshmallow import ValidationError

from yafas.auth.error_handlers import handlers as auth_error_handlers

from .orm import InstanceNotFound


def marshmallow_validation_handler(exception, request, response, params):
    response.media = exception.messages
    response.status = falcon.HTTP_400


def instance_not_found_handler(exception, request, response, params):
    response.media = {'message': ['Not found']}
    response.status = falcon.HTTP_404


handlers = (
    (ValidationError, marshmallow_validation_handler),
    (InstanceNotFound, instance_not_found_handler),
    *auth_error_handlers,
)
