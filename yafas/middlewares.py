from yafas.auth.middlewares import JWTTokenMiddleware
from yafas.orm import SQLAlchemySessionMiddleware

middlewares = [
    JWTTokenMiddleware(),
    SQLAlchemySessionMiddleware(),
]
