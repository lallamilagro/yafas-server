from yafas.auth.models import User


def test_create_access_token(factory):
    user = factory.user()
    token = user.create_access_token()

    decoded = User.decode_token(token)

    assert decoded['sub'] == user.email
    assert decoded['type'] == 'access'


def test_jwt_retrieve(factory):
    user = factory.user()
    token = user.create_access_token()

    assert User.retrieve_by_token(token) == user
