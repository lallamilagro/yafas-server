import pytest
from mixer.backend.flask import mixer as flask_mixer

from tests import ApiClient, Factory
from yafas import YafasApp, db as yafas_db

app_config = dict(
    MIGRATIONS_DIR='yafas/migrations/',
    SECRET_KEY='12345',
    SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    BCRYPT_LOG_ROUNDS=4,
)


@pytest.fixture(scope='session', autouse=True)
def app() -> YafasApp:
    app = YafasApp('yafas', config=app_config)
    app.app_context().push()

    app.test_client_class = ApiClient

    yafas_db.create_all()

    return app


@pytest.fixture
def db():
    savepoint = yafas_db.session.begin_nested()
    for _ in range(2):
        yafas_db.session.begin_nested()
    yield yafas_db
    savepoint.rollback()


@pytest.fixture
def mixer():
    return flask_mixer


@pytest.fixture
def factory(db):
    return Factory(db)


@pytest.fixture
def client(app):
    return app.test_client()
