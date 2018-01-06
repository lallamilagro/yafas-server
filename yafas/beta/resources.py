from flask import request
from flask_restful import Resource

from .schemas import RegistrationSchema


class Registration(Resource):

    def post(self):
        beta, errors = RegistrationSchema().load(request.json)
        return (errors, 400) if errors else ({}, 201)
