from unittest.mock import patch

import freezegun
import pytest
from mixer.backend.sqlalchemy import Mixer
from sqlalchemy import event

from tests import Factory
from yafas import config as yafas_config, db as yafas_db
from yafas.app import YafasApp


@pytest.fixture(scope='session', autouse=True)
def config() -> dict:
    overrides = {
        'BCRYPT_ROUNDS': 4,
        'SECRET_KEY': 'azaza',
        'DATABASE_URI': 'sqlite:///:memory:',
        'DATABASE_ECHO': True,
    }

    with patch.dict(yafas_config, overrides):
        yield yafas_config


@pytest.fixture(scope='session', autouse=True)
def app(config) -> YafasApp:
    return YafasApp()


@pytest.fixture
def api(app):
    return app.api


@pytest.fixture(autouse=True)
def db(app):
    """Manually creates db connection, start transaction and configre
    session to use it."""
    connection = app.engine.connect()
    transaction = connection.begin()
    yafas_db.session.configure(bind=connection)

    for _ in range(2):
        yafas_db.session.begin_nested()

    yield yafas_db

    transaction.rollback()
    connection.close()
    yafas_db.session.remove()


@pytest.fixture
def skip_rollback(db):
    """Skips all rallback calls."""
    @event.listens_for(yafas_db.session, 'after_transaction_end')
    def restart_savepoint(session, transaction):
        """Start new nested transaction when `transaction` rolled back.

        As a side effect `db.session.rollback()` does not work inside tests.
        """
        if transaction.nested:
            session.begin_nested()


@pytest.fixture
def mixer(db):
    return Mixer(db.session, commit=True)


@pytest.fixture
def factory(db):
    return Factory()


@pytest.fixture
def freeze_time():
    return freezegun.freeze_time
