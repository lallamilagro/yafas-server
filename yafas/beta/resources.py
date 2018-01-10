from flask import request
from flask.views import MethodView

from .schemas import RegistrationSchema


class Registration(MethodView):

    def post(self):
        beta, errors = RegistrationSchema().load(request.json)
        return (errors, 400) if errors else ({}, 201)
