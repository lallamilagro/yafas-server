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


@pytest.mark.parametrize('count', range(1, 10))
@pytest.mark.usefixtures('skip_rollback')
def test_rollback_can_be_skipped(count, db, factory):
    factory.cycle(count).user()

    assert db.session.query(User).count() == count

    db.session.rollback()

    assert db.session.query(User).count() == count


def test_db_configured(app, config, db):
    assert str(app.engine.url) == 'sqlite:///:memory:'
    assert str(db.session.bind.engine.url) == 'sqlite:///:memory:'
