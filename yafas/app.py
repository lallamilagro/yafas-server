import falcon

from . import db
from .error_handlers import handlers
from .middlewares import middlewares
from .routes import routes


class YafasApp:

    def __init__(self):
        self.api = falcon.API(middleware=middlewares)

        self.init_resources()
        self.init_error_handlers()

        db.init()

    def init_resources(self):
        for uri, resource in routes:
            self.api.add_route(f'/api/v1/{uri}/', resource)

    def init_error_handlers(self):
        for exception, handler in handlers:
            self.api.add_error_handler(exception, handler)
