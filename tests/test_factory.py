import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('count', range(1, 10))
def test_cycle_factory(count, factory):
    users = factory.cycle(count).user()

    assert len(users) == count
    assert User.query.count() == count
    for user in users:
        assert isinstance(user, User)


def test_factory(factory):
    user = factory.user()

    assert isinstance(user, User)
    assert User.query.count() == 1
