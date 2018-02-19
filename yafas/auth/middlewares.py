from . import exceptions
from .models import User


class JWTTokenMiddleware:

    def parse_token(self, req) -> str:
        auth = req.headers.get('AUTHORIZATION')  # type: str
        return auth.split(' ')[-1]

    def handle_required_type(self, token: str, required_type: str):
        token_type = User.decode_token(token)['type']

        if token_type != required_type:
            raise exceptions.JWTInvalidTokenType(
                f'Only {required_type} tokens can access this endpoint')

    def process_resource(self, req, res, resource, params):
        if req.method == 'OPTIONS':
            return

        required_type = getattr(resource, 'required_token', 'access')
        if not required_type:
            return

        token = self.parse_token(req)
        self.handle_required_type(token, required_type)

        resource.user = User.retrieve_by_token(token)
