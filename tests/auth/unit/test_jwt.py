import pytest

from yafas.auth.models import User


@pytest.mark.parametrize('token_type', ('access', 'refresh'))
def test_create_token(token_type, factory):
    user = factory.user()
    token = getattr(user, f'create_{token_type}_token')()

    decoded = User.decode_token(token)

    assert decoded['sub'] == user.email
    assert decoded['type'] == token_type


@pytest.mark.freeze_time('2020-01-01')
def test_tokens_are_different(factory):
    user = factory.user()

    assert user.create_access_token() != user.create_refresh_token()


@pytest.mark.parametrize('token_type', ('access', 'refresh'))
def test_jwt_retrieve(token_type, factory):
    user = factory.user()
    token = getattr(user, f'create_{token_type}_token')()

    assert User.retrieve_by_token(token) == user
