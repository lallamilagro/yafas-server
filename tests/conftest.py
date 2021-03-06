from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from mixer.backend.sqlalchemy import mixer as sqlalchemy_mixer

from tests import Factory
from yafas import config as yafas_config, db as yafas_db
from yafas.app import YafasApp


@pytest.fixture(scope='session', autouse=True)
def config() -> dict:
    overrides = {
        'ACCESS_TOKEN_EXPIRES': timedelta(days=30),
        'ALLOW_ORIGIN': 'http://test.yafas.org',
        'BCRYPT_ROUNDS': 4,
        'DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'lolkekcheburek',
        'SECURE_COOKIES': True,
        'COOKIES_DOMAIN': 'yafas.org',
    }

    with patch.dict(yafas_config, overrides):
        yield yafas_config


@pytest.fixture(scope='session', autouse=True)
def app(config) -> YafasApp:
    app = YafasApp()

    yafas_db.create()

    return app


@pytest.fixture
def api(app):
    return app.api


@pytest.fixture(autouse=True)
def db(app):
    """Manually creates db connection, start transaction and configre
    session to use it."""
    connection = yafas_db.engine.connect()
    transaction = connection.begin()
    yafas_db.session.configure(bind=connection)

    for _ in range(2):
        yafas_db.session.begin_nested()

    yield yafas_db

    transaction.rollback()
    connection.close()
    yafas_db.session.remove()


@pytest.fixture
def mixer(db):
    return sqlalchemy_mixer


@pytest.fixture
def factory(db):
    return Factory()


@pytest.fixture
def now():
    return datetime.utcnow()


@pytest.fixture
def ApiTestClientCls(ApiTestClientCls, config):

    class ApiTestClient(ApiTestClientCls):

        def response_assertions(self, response):
            assert response.headers[
                'Access-Control-Allow-Origin'] == config['ALLOW_ORIGIN']
            assert response.headers[
                'Access-Control-Allow-Credentials'] == 'true'
            assert 'Content-Type' in response.headers[
                'Access-Control-Allow-Headers']

            allow = response.headers.get('allow', None)
            if allow:
                assert response.headers[
                    'Access-Control-Allow-Methods'] == allow

        def prepare_request(self, method, expected, *args, **kwargs):
            user = kwargs.pop('user', None)

            if user:
                access_token = user.create_access_token()
                headers = kwargs.get('headers', {})
                headers['cookie'] = f'access_token={access_token}'
                kwargs['headers'] = headers

            return args, kwargs

    return ApiTestClient
