from unittest.mock import patch

import freezegun
import pytest
from mixer.backend.flask import mixer as flask_mixer

from tests import Factory
from yafas import config as yafas_config, db as yafas_db
from yafas.app import YafasApp


@pytest.fixture(scope='session', autouse=True)
def config() -> dict:
    overrides = {
        'BCRYPT_ROUNDS': 4,
        'SECRET_KEY': 'azaza',
    }

    with patch.dict(yafas_config, overrides):
        yield


@pytest.fixture(scope='session', autouse=True)
def app(config) -> YafasApp:
    return YafasApp()


@pytest.fixture
def api(app):
    return app.api


@pytest.fixture
def db():
    savepoint = yafas_db.session().begin_nested()
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
def freeze_time():
    return freezegun.freeze_time
