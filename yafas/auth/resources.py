import falcon

from . import CookieCreator, models, schemas


class AuthCookiesMixin:

    schema = None
    require_token = None

    def cookies_data(self, request) -> dict:
        token, _ = self.schema().load(request.media)
        return CookieCreator(token)()

    def set_cookies(self, request, response):
        cookies_data = self.cookies_data(request)

        for cookie_name, cookie_data in cookies_data.items():
            response.set_cookie(cookie_name, **cookie_data)


class CheckEmail:
    require_token = None

    def on_get(self, request, response, email):
        schemas.EmailSchema().load({'email': email})
        response.media = {}


class Login(AuthCookiesMixin):
    schema = schemas.LoginSchema

    def on_post(self, request, response):
        self.set_cookies(request, response)
        response.status = falcon.HTTP_201


class Register(AuthCookiesMixin):
    schema = schemas.RegistrationSchema

    def on_post(self, request, response):
        self.set_cookies(request, response)
        response.status = falcon.HTTP_201


class Info:

    def on_get(self, request, response):
        user = models.User.query.get(request.user_id)
        response.media, _ = schemas.UserInfoSchema().dump(user)
