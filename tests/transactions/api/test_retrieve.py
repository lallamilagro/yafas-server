from decimal import Decimal

import pytest


def url(id: int=None) -> str:
    _url = '/api/v1/transactions/'
    return _url + f'{id}/' if id else _url


@pytest.mark.parametrize('value, expected', (
    (Decimal('100'), 100),
    (Decimal('100.34'), 100.34),
    (Decimal('0.34'), 0.34),
))
def test_retrieve(value, expected, client, freezer, now, user_and_transaction):
    freezer.move_to(now)
    user, transaction = user_and_transaction(value=value)

    got = client.get(url(transaction.id), user=user)

    assert got['id'] == transaction.id
    assert got['value'] == expected
    assert got['created_at'] == f'{now.isoformat()}+00:00'


def test_retrieve_for_current_user_only(client, user_and_transaction):
    user0, transaction0 = user_and_transaction()
    user1, transaction1 = user_and_transaction()

    response = client.get(url(transaction0.id), user=user1, as_response=True)

    assert response.status_code == 404
    assert response.json == {'message': ['Not found']}
