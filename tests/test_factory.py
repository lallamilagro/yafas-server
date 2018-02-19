import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('commit', (False, True))
@pytest.mark.parametrize('count', range(1, 4))
def test_cycle_factory(count, commit, factory, db):
    users = factory.cycle(count).user()
    if commit:
        db.session.commit()

    assert len(users) == count
    User.query.count() == count
    for user in users:
        assert isinstance(user, User)


@pytest.mark.parametrize('commit', (False, True))
def test_factory(commit, factory, db):
    user = factory.user()
    if commit:
        db.session.commit()

    assert isinstance(user, User)
    assert User.query.count() == 1
