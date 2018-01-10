from flask import Blueprint
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class AuthBlueprint(Blueprint):

    def register(self, app, *args, **kwargs):
        bcrypt.init_app(app)
        super().register(app, *args, **kwargs)


bp = AuthBlueprint('auth', __name__)

from .resources import CheckEmail  # noqa  # isort:skip
check_email = CheckEmail.as_view('check_email')
bp.add_url_rule(
    '/check-email/<email>/', view_func=check_email, methods=['GET'])
