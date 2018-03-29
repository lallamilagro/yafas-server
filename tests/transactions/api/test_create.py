from yafas.transactions.models import Transaction

URL = '/api/v1/transactions/'


def test_create(client, freezer, now, db, factory):
    freezer.move_to(now)
    user = factory.user()

    got = client.post(URL, json={'value': 123.45}, user=user)

    assert Transaction.query.filter_by(id=got['id'], user_id=user.id).first()


def test_create_returns_instance(client, freezer, now, db, factory):
    user = factory.user()

    got = client.post(URL, json={'value': 123.45}, user=user)

    assert got['value'] == 123.45
    assert got['created_at'] == f'{now.isoformat()}+00:00'
