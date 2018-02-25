import pytest

from tests import cors_callback
from yafas.auth.models import User

pytestmark = pytest.mark.client(callback=cors_callback)

URL = '/api/v1/auth/login/'


@pytest.fixture
def user(db, factory):
    return factory.user(email='test@test.com', password='test')


def test_login_returns_cookie_token(client, user):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    token_cookie = response.cookies['access_token']

    assert token_cookie.name == 'access_token'
    assert token_cookie.http_only
    assert token_cookie.secure

    assert User.retrieve_by_token(token_cookie.value).id == user.id


def test_login_response_media(client, user):
    got = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    })

    assert got == {}


@pytest.mark.parametrize('credentials', [
    dict(email='test@test.ru', password='test'),
    dict(email='test@test.com', password='watwatwat'),
])
def test_invalid_credential(credentials, client):
    response = client.post(URL, json=credentials, as_response=True)

    assert response.status_code == 400
    assert response.json == {'message': ['Not a valid credentials.']}
    assert not response.cookies


def test_options_works(client):
    client.options(URL)
