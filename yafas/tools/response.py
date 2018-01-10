from flask import Response
from flask.json import jsonify


class JsonResponse(Response):

    default_mimetype = 'application/json'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_cors()

    def _set_cors(self):
        self.headers.set('Access-Control-Allow-Origin', '*')
        self.headers.set('Access-Control-Allow-Headers', 'CONTENT-TYPE')

    @classmethod
    def force_type(cls, response, environ=None):
        return super().force_type(jsonify(response), environ)
