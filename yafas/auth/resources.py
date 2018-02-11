import falcon

from . import schemas


class CheckEmail:
    required_token = None

    def on_get(self, request, response, email):
        schemas.EmailSchema().load({'email': email})
        response.media = {}


class Login:
    required_token = None

    def on_post(self, request, response):
        response.media, _ = schemas.LoginSchema().load(
            request.media)
        response.status = falcon.HTTP_201


class Register:
    required_token = None

    def on_post(self, request, response):
        response.media, _ = schemas.RegistrationSchema().load(
            request.media)
        response.status = falcon.HTTP_201


class Refresh:
    required_token = 'refresh'

    def on_post(self, request, response):
        response.media = {
            'access_token': self.user.create_access_token(),
            'refresh_token': self.user.create_refresh_token(),
        }
        response.status = falcon.HTTP_201
