import sqlalchemy as sa
from sqlalchemy import orm

from yafas import db
from yafas.auth.models import User


class BetaUser(db.Model):
    __tablename__ = 'beta_users'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)

    user = orm.relationship(User, backref=orm.backref('beta', uselist=False))

    def __init__(self, email: str, password: str):
        self.user = User(email=email, password=password, active=True)
