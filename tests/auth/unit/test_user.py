import datetime


def test_registered_in_propery_auto_installed(freeze_time, factory):
    now = datetime.datetime.utcnow()
    with freeze_time(now):
        user = factory.user()

    assert user.registered_in == now


def test_password_hashed(factory):
    user = factory.user(password='test')

    assert user.password != 'test'


def test_check_password(factory):
    user = factory.user(password='test')

    assert user.check_password('test')
    assert not user.check_password('shit')


def test_user_active_by_default(factory):
    user = factory.user()

    assert user.active is True


def test_user_can_be_inactive(factory):
    user = factory.user(active=False)

    assert user.active is False
