import falcon

from . import schemas


class CheckEmail:
    require_token = None

    def on_get(self, request, response, email):
        schemas.EmailSchema().load({'email': email})
        response.media = {}


class Login:
    require_token = None

    def on_post(self, request, response):
        token, _ = schemas.LoginSchema().load(
            request.media)
        response.set_cookie('access_token', token)
        response.status = falcon.HTTP_201


class Register:
    require_token = None

    def on_post(self, request, response):
        token, _ = schemas.RegistrationSchema().load(
            request.media)
        response.set_cookie('access_token', token)
        response.status = falcon.HTTP_201


class Info:

    def on_get(self, request, response):
        response.media, _ = schemas.UserInfoSchema().dump(self.user())
