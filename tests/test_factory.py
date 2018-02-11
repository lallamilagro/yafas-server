import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('count', range(1, 10))
def test_cycle_factory(count, factory, db):
    users = factory.cycle(count).user()

    assert len(users) == count
    db.session.query(User).count() == count
    for user in users:
        assert isinstance(user, User)


def test_factory(factory, db):
    user = factory.user()

    assert isinstance(user, User)
    assert db.session.query(User).count() == 1
