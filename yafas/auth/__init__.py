import importlib

from flask import Blueprint
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class AuthBlueprint(Blueprint):

    def register(self, app, *args, **kwargs):
        bcrypt.init_app(app)
        importlib.import_module(f'{__name__}.models')
        super().register(app, *args, **kwargs)


bp = AuthBlueprint('auth', __name__)
