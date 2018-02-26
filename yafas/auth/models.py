import datetime

import bcrypt
import jwt
import sqlalchemy as sa

from yafas import config, db


class User(db.Base):
    __tablename__ = 'users'

    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    registered_in = sa.Column(sa.DateTime, nullable=False)
    active = sa.Column(sa.Boolean, default=True, nullable=False)

    def __init__(self, email: str, password: str, active: bool=None):
        self.email = email
        self.password = self.__hash_password(password)
        self.registered_in = datetime.datetime.utcnow()

        self.active = active

    def __hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(config['BCRYPT_ROUNDS']),
        )

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password)

    def __create_token(self, token_type: str, expires_delta) -> bytes:
        now = datetime.datetime.utcnow()
        payload = {
            'exp': now + expires_delta,
            'iat': now,
            'sub': self.email,
            'type': token_type,
        }
        return jwt.encode(
            payload,
            config['SECRET_KEY'],
            algorithm='HS256',
        ).decode()

    def create_access_token(self) -> str:
        return self.__create_token('access', config['ACCESS_TOKEN_EXPIRES'])

    @classmethod
    def decode_token(cls, token: str) -> dict:
        return jwt.decode(token.encode(), config['SECRET_KEY'])

    @classmethod
    def retrieve_by_token(cls, token: str) -> 'User':
        decoded = cls.decode_token(token)
        return cls.query.filter_by(email=decoded['sub']).first()
