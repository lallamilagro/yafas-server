import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('count', range(1, 4))
def test_objects_removed_between_tests(app, count, factory, db):
    factory.cycle(count).user()

    assert db.session.query(User).count() == count


@pytest.mark.parametrize('count', range(1, 4))
def test_commited_objects_removed_between_tests(app, count, factory, db):
    factory.cycle(count).user()
    db.session.commit()

    assert db.session.query(User).count() == count


@pytest.mark.parametrize('count', range(1, 4))
def test_rollback_works(count, db, factory):
    factory.cycle(count).user()

    assert db.session.query(User).count() == count

    db.session.rollback()

    assert db.session.query(User).count() == 0


@pytest.mark.parametrize('count', range(1, 4))
def test_rollback_works_with_commit(count, db, factory):
    factory.cycle(count).user()
    db.session.commit()

    assert db.session.query(User).count() == count

    db.session.rollback()

    assert db.session.query(User).count() == 0


@pytest.mark.parametrize('count', range(1, 4))
def test_rollback_works_with_nested(count, db, factory):
    db.session.begin_nested()
    factory.cycle(count).user()
    db.session.commit()

    assert db.session.query(User).count() == count

    db.session.rollback()

    assert db.session.query(User).count() == 0


def test_and_now_db_clean(db):
    assert db.session.query(User).count() == 0


def test_db_configured(app, config, db):
    assert str(app.engine.url) == 'sqlite:///:memory:'
    assert str(db.session.bind.engine.url) == 'sqlite:///:memory:'
