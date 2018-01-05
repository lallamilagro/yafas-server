import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('count', range(1, 10))
def test_objects_removed_between_tests(count, factory):
    factory.cycle(count).user()
    assert User.query.count() == count


@pytest.mark.parametrize('count', range(1, 10))
def test_rollback_work_inside_tests(count, db, factory):
    factory.cycle(count).user()

    assert User.query.count() == count

    db.session.rollback()

    assert User.query.count() == 0
