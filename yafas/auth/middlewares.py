from . import exceptions
from .models import User


class JWTCookieMiddleware:

    def validate_token(self, token: str):
        User.decode_token(token)

    def set_user_method(self, resource, token: str):
        resource.user = lambda: User.retrieve_by_token(token)

    def load_token(self, request):
        token = request.cookies.get('access_token')
        if not token:
            raise exceptions.JWTNoTokens('No tokens passed')
        return token

    def process_resource(self, request, response, resource, params):
        if request.method == 'OPTIONS':
            return

        require_token = getattr(resource, 'require_token', True)
        if not require_token:
            return

        token = self.load_token(request)

        self.validate_token(token)
        self.set_user_method(resource, token)
