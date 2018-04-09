from datetime import timedelta

from yafas.transactions.models import Transaction


def test_create(client, db, factory, now, url):
    user = factory.user()

    new_date = (now + timedelta(days=2)).date()
    got = client.post(
        url(),
        json={'value': 123.45, 'on_date': new_date.isoformat()},
        user=user)

    assert Transaction.query.filter_by(
        id=got['id'],
        on_date=new_date,
        user_id=user.id,
    ).first()


def test_create_with_required_only(client, db, factory, url):
    user = factory.user()

    got = client.post(url(), json={'value': 123.45}, user=user)

    assert Transaction.query.filter_by(id=got['id'], user_id=user.id).first()


def test_create_with_null_date(client, db, factory, now, url):
    user = factory.user()

    got = client.post(
        url(),
        json={'value': 123.45, 'on_date': None},
        user=user,
    )

    assert Transaction.query.filter_by(
        id=got['id'],
        on_date=now.date(),
        user_id=user.id,
    ).first()


def test_create_returns_instance(client, db, factory, freezer, now, url):
    freezer.move_to(now)
    user = factory.user()

    got = client.post(url(), json={'value': 123.45}, user=user)

    assert got['value'] == 123.45
    assert got['on_date'] == f'{now.date().isoformat()}'
