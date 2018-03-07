from yafas.auth.models import User


class CookieCreator:

    def __init__(self, token: str):
        self.token = token

    def expires(self) -> dict:
        return User.decode_token(self.token)['exp']

    def __call__(self) -> dict:
        base_kw = {
            'secure': True,
            'path': '/',
            'max_age': self.expires(),
        }
        return {
            'access_token': dict(value=self.token, http_only=True, **base_kw),
            'logged_in': dict(value='true', http_only=False, **base_kw),
        }
