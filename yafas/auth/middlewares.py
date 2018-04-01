from . import exceptions
from .models import User


class JWTCookieMiddleware:

    def decode_token(self, token: str) -> dict:
        return User.decode_token(token)

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

        token_payload = self.decode_token(token)
        request.user_id = token_payload['sub']
