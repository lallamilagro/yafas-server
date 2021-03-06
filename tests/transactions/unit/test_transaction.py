from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError


@pytest.mark.parametrize('value, expected', (
    (123, Decimal('123')),
    (12.34, Decimal('12.34')),
))
def test_value(value, expected, factory):
    transaction = factory.transaction(value=value)

    assert transaction.value == expected


def test_on_date_is_auto_installed(freezer, now, factory):
    freezer.move_to(now)

    transaction = factory.transaction()

    assert transaction.on_date == now.date()


def test_user_relation(factory):
    user = factory.user()

    transaction = factory.transaction(user_id=user.id)
    assert transaction.user == user


def test_transactions_relation_of_user(factory):
    user = factory.user()
    transactions = factory.cycle(2).transaction(user_id=user.id)

    assert len(user.transactions) == 2
    for transaction in transactions:
        assert transaction in user.transactions


def test_user_constraint(db, factory):
    with pytest.raises(IntegrityError):
        factory.transaction(user_id=100500)
