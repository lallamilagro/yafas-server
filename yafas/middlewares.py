from yafas.auth.middlewares import JWTTokenMiddleware
from yafas.orm import SQLAlchemySessionMiddleware


class CORSMiddleware:

    def process_response(self, request, response, *args, **kwargs):
        response.set_headers({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': ('CONTENT-TYPE', 'Authorization'),
        })


middlewares = [
    JWTTokenMiddleware(),
    SQLAlchemySessionMiddleware(),
    CORSMiddleware(),
]
