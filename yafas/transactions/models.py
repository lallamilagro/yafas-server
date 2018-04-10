from datetime import date, datetime
from decimal import Decimal
from typing import Union

import sqlalchemy as sa

from yafas import db


class Transaction(db.Base):
    __tablename__ = 'transactions'

    on_date = sa.Column(sa.Date, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    value = sa.Column(sa.Numeric(precision=8, scale=2), nullable=False)

    user = sa.orm.relationship('User', back_populates='transactions')

    def __init__(
            self, value: Union[float, Decimal], user_id: int,
            on_date: date=None):
        self.value = value
        self.user_id = user_id
        self.on_date = on_date or datetime.utcnow().date()
