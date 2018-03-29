from yafas.transactions.models import Transaction


def test_create(client, db, factory, freezer, now, url):
    freezer.move_to(now)
    user = factory.user()

    got = client.post(url(), json={'value': 123.45}, user=user)

    assert Transaction.query.filter_by(id=got['id'], user_id=user.id).first()


def test_create_returns_instance(client, db, factory, freezer, now, url):
    user = factory.user()

    got = client.post(url(), json={'value': 123.45}, user=user)

    assert got['value'] == 123.45
    assert got['created_at'] == f'{now.isoformat()}+00:00'
