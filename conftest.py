import pytest

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

    yafas_db.create_all()

    return app


@pytest.fixture
def db():
    savepoint = yafas_db.session.begin_nested()
    for _ in range(2):
        yafas_db.session.begin_nested()
    yield yafas_db
    savepoint.rollback()
