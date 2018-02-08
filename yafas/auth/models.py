import datetime

import bcrypt
import sqlalchemy as sa

from yafas.orm import db


class User(db.Base):
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
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=4))

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password)

    # def create_access_token(self) -> str:
    #     return create_access_token(identity=self.email)

    # def create_refresh_token(self) -> str:
    #     return create_refresh_token(identity=self.email)

    # @classmethod
    # def jwt_retrieve(cls) -> 'User':
    #     return cls.query.filter_by(email=get_jwt_identity()).first()
