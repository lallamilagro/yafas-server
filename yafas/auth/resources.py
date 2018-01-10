from flask.views import MethodView

from .schemas import EmailSchema


class CheckEmail(MethodView):

    def get(self, email: str):
        _, errors = EmailSchema().load({'email': email})
        return (errors, 400) if errors else ({}, 200)
