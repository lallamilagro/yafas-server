import datetime

from freezegun import freeze_time

from yafas.auth.models import User


def test_registered_in_propery_auto_installed(db):
    now = datetime.datetime.utcnow()
    with freeze_time(now):
        user = User(email='test@test.com', password='test')

    assert user.registered_in == now

    db.session.add(user)
    db.session.commit()

    assert user.registered_in == now


def test_password_hashed(user):
    assert user.password != 'test'


def test_check_password(user):
    assert user.check_password('test')
    assert not user.check_password('shit')
