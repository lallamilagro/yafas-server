from yafas.auth.middlewares import JWTCookieMiddleware
from yafas.orm import SQLAlchemySessionMiddleware


class DefaultResponseJsonMiddleware:

    def process_response(self, request, response, *args, **kwargs):
        if response.media is None:
            response.media = {}


class CORSMiddleware:

    def process_response(self, request, response, *args, **kwargs):
        response.set_headers({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        })


middlewares = [
    JWTCookieMiddleware(),
    SQLAlchemySessionMiddleware(),
    CORSMiddleware(),
    DefaultResponseJsonMiddleware(),
]
