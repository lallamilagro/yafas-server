import falcon

from yafas import config
from yafas.auth.middlewares import JWTCookieMiddleware
from yafas.orm import SQLAlchemySessionMiddleware


class DefaultResponseJsonMiddleware:

    def process_response(self, request, response, *args, **kwargs):
        if response.media is None and response.status != falcon.HTTP_204:
            response.media = {}


class CORSMiddleware:

    def allow_orogin_value(self, request) -> str:
        return request.headers.get('ORIGIN', config['ALLOW_ORIGIN'])

    def process_response(self, request, response, *args, **kwargs):
        response.set_headers({
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': self.allow_orogin_value(request),
            'Access-Control-Allow-Headers': 'Content-Type',
        })


middlewares = [
    JWTCookieMiddleware(),
    SQLAlchemySessionMiddleware(),
    CORSMiddleware(),
    DefaultResponseJsonMiddleware(),
]
