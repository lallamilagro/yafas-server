from flask import Response
from flask.json import jsonify
from werkzeug.exceptions import HTTPException


class JsonResponse(Response):

    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, response, environ=None):
        if not isinstance(response, HTTPException):
            response = jsonify(response)

        return super().force_type(response, environ)


def apply_cors(response):
    response.headers.set('Access-Control-Allow-Origin', '*')
    response.headers.set(
        'Access-Control-Allow-Headers', 'CONTENT-TYPE,Authorization')
    return response
