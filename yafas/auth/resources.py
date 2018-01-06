from flask_restful import Resource

from .schemas import EmailSchema


class CheckEmail(Resource):

    def get(self, email: str):
        _, errors = EmailSchema().load({'email': email})
        return (errors, 400) if errors else ({}, 200)
