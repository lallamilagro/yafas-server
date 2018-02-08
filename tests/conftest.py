import freezegun
import pytest
from mixer.backend.flask import mixer as flask_mixer

from tests import Factory
from yafas import orm
from yafas.app import YafasApp

app_config = dict(
    DATABASE_URI='sqlite:///:memory:',
)


@pytest.fixture(scope='session', autouse=True)
def app() -> YafasApp:
    return YafasApp(config=app_config)


@pytest.fixture
def api(app):
    return app.api


@pytest.fixture
def db():
    savepoint = orm.db.session().begin_nested()
    for _ in range(2):
        orm.db.session.begin_nested()
    yield orm.db
    savepoint.rollback()


@pytest.fixture
def mixer():
    return flask_mixer


@pytest.fixture
def factory(db):
    return Factory(db)


@pytest.fixture
def freeze_time():
    return freezegun.freeze_time
