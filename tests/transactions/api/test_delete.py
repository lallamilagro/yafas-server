from yafas.transactions.models import Transaction


def url(id: int=None) -> str:
    _url = '/api/v1/transactions/'
    return _url + f'{id}/' if id else _url


def test_delete(client, db, user_and_transaction):
    user, transaction = user_and_transaction()

    client.delete(url(transaction.id), user=user)

    assert not Transaction.query.get(transaction.id)


def test_delete_for_current_user_only(client, user_and_transaction):
    user0, transaction0 = user_and_transaction()
    user1, transaction1 = user_and_transaction()

    response = client.delete(
        url(transaction0.id),
        user=user1,
        as_response=True,
    )

    assert response.status_code == 404
    assert response.json == {'message': ['Not found']}
