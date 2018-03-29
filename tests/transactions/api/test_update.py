from decimal import Decimal


def url(id: int=None) -> str:
    _url = '/api/v1/transactions/'
    return _url + f'{id}/' if id else _url


def test_update(client, db, user_and_transaction):
    user, transaction = user_and_transaction()

    client.put(url(transaction.id), json={'value': 123.45}, user=user)

    assert transaction.value == Decimal('123.45')


def test_update_returns_the_same_instance(client, db, user_and_transaction):
    user, transaction = user_and_transaction()

    got = client.put(url(transaction.id), json={'value': 123.45}, user=user)

    assert got['id'] == transaction.id
    assert got['value'] == 123.45


def test_retrieve_for_current_user_only(client, user_and_transaction):
    user0, transaction0 = user_and_transaction()
    user1, transaction1 = user_and_transaction()

    response = client.put(
        url(transaction0.id),
        json={'value': 123.45},
        user=user1,
        as_response=True,
    )

    assert response.status_code == 404
    assert response.json == {'message': ['Not found']}
