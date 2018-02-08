# from flask import Blueprint
# from flask_bcrypt import Bcrypt
# from flask_jwt_extended import JWTManager

# bcrypt = Bcrypt()
# jwt = JWTManager()


# class AuthBlueprint(Blueprint):

#     def register(self, app, *args, **kwargs):
#         bcrypt.init_app(app)
#         jwt.init_app(app)
#         super().register(app, *args, **kwargs)


# bp = AuthBlueprint('auth', __name__)

# from . import resources  # noqa  # isort:skip
