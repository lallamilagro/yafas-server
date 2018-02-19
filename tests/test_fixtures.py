import pytest

from yafas.auth.models import User


def test_db_configured(config, db):
    assert str(db.engine.url) == config['DATABASE_URI']
    assert str(db.session.bind.engine.url) == config['DATABASE_URI']


@pytest.mark.parametrize('commit', (False, True))
@pytest.mark.parametrize('count', range(1, 4))
def test_objects_removed_between_tests(commit, count, factory, db):
    factory.cycle(count).user()
    if commit:
        db.session.commit()

    assert User.query.count() == count


@pytest.mark.parametrize('commit', (False, True))
@pytest.mark.parametrize('count', range(1, 4))
def test_rollback_works(commit, count, db, factory):
    factory.cycle(count).user()
    if commit:
        db.session.commit()

    assert User.query.count() == count

    db.session.rollback()

    assert User.query.count() == 0


def test_and_now_db_clean():
    assert User.query.count() == 0
