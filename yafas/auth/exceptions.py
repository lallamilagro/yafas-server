class JWTException(Exception):
    pass


class JWTNoTokens(JWTException):
    pass
