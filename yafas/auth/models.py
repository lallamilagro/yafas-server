import datetime

import sqlalchemy as sa
from flask import current_app

from yafas import db

from . import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    password = sa.Column(sa.String(255), nullable=False)
    registered_in = sa.Column(sa.DateTime, nullable=False)
    active = sa.Column(sa.Boolean, default=True, nullable=False)

    def __init__(self, email: str, password: str, active: bool=None):
        self.email = email
        self.password = self.__hash_password(password)
        self.registered_in = datetime.datetime.utcnow()

        self.active = active

    def __hash_password(self, password: str) -> str:
        return bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)
