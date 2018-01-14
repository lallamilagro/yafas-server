import pytest

from yafas import YafasApp, db


@pytest.fixture
def config():
    return dict(
        BCRYPT_LOG_ROUNDS=4,
        JWT_SECRET_KEY='I-hate-frontend',
        MIGRATIONS_DIR='yafas/migrations/',
        SECRET_KEY='12345',
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )


@pytest.mark.parametrize('option, expected', (
    ('BCRYPT_LOG_ROUNDS', 4),
    ('JWT_SECRET_KEY', 'I-hate-frontend'),
    ('MIGRATIONS_DIR', 'yafas/migrations/'),
    ('SECRET_KEY', '12345'),
    ('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:'),
    ('SQLALCHEMY_TRACK_MODIFICATIONS', False),
))
def test_app_configuration(option, expected, config):
    app = YafasApp('yafas', config=config)

    assert app.config.get(option) == expected


def test_db_configured(config):
    app = YafasApp('yafas', config=config)

    with app.app_context():
        assert str(db.engine.url) == 'sqlite:///:memory:'
        assert str(db.session.bind.engine.url) == 'sqlite:///:memory:'
