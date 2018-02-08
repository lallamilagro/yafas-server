import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('count', range(1, 10))
def test_objects_removed_between_tests(app, count, factory, db):
    factory.cycle(count).user()

    assert db.session.query(User).count() == count


@pytest.mark.parametrize('count', range(1, 10))
def test_rollback_work_inside_tests(count, db, factory):
    factory.cycle(count).user()

    assert db.session.query(User).count() == count

    db.session.rollback()

    assert db.session.query(User).count() == 0
