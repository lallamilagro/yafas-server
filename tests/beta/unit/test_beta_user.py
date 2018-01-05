import datetime

from freezegun import freeze_time

from yafas.beta.models import BetaUser


def test_created_with_user(db):
    beta = BetaUser(email='test@test.com', password='test')
    db.session.add(beta)
    db.session.commit()

    assert beta.id
    assert beta.user_id


def test_user_created_correctly(db):
    now = datetime.datetime.utcnow()
    with freeze_time(now):
        beta = BetaUser(email='test@test.com', password='test')
    db.session.add(beta)
    db.session.commit()

    assert beta.user.email == 'test@test.com'
    assert beta.user.registered_in == now
    assert beta.user.active is True
