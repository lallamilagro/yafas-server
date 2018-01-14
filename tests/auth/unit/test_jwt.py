def test_create_access_token(factory):
    user = factory.user()

    assert isinstance(user.create_access_token(), str)


def test_create_refresh_token(factory):
    user = factory.user()

    assert isinstance(user.create_refresh_token(), str)


def test_tokens_are_different(factory):
    user = factory.user()

    assert user.create_access_token() != user.create_refresh_token()
