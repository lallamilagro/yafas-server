from flask import Blueprint
from flask_bcrypt import Bcrypt
from flask_restful import Api

bcrypt = Bcrypt()


class AuthBlueprint(Blueprint):

    def register(self, app, *args, **kwargs):
        bcrypt.init_app(app)
        super().register(app, *args, **kwargs)


bp = AuthBlueprint('auth', __name__)

api = Api(bp)

from .resources import CheckEmail  # noqa  # isort:skip
api.add_resource(CheckEmail, '/check-email/<email>/')
