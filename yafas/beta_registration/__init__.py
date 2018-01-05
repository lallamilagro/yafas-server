import importlib

from flask import Blueprint


class BetaRegistrationBlueprint(Blueprint):

    def register(self, app, *args, **kwargs):
        importlib.import_module(f'{__name__}.models')
        super().register(app, *args, **kwargs)


bp = BetaRegistrationBlueprint('beta_registration', __name__)
