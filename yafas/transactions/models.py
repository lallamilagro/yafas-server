from datetime import datetime
from decimal import Decimal
from typing import Union

import sqlalchemy as sa

from yafas import db


class Transaction(db.Base):
    __tablename__ = 'transactions'

    created_at = sa.Column(sa.DateTime, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    value = sa.Column(sa.Numeric(precision=8, scale=2), nullable=False)

    user = sa.orm.relationship('User', back_populates='transactions')

    def __init__(self, value: Union[float, Decimal], user_id: int):
        self.value = value
        self.user_id = user_id
        self.created_at = datetime.utcnow()
