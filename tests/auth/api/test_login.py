from datetime import datetime

import pytest

from yafas.auth.models import User

URL = '/api/v1/auth/login/'


@pytest.fixture
def user(db, factory):
    return factory.user(email='test@test.com', password='test')


def test_login_returns_cookie_token(config, client, user):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    token_cookie = response.cookies['access_token']

    assert token_cookie.name == 'access_token'
    assert token_cookie.http_only
    assert token_cookie.secure
    assert token_cookie.path == '/'
    assert token_cookie.domain == 'yafas.org'

    assert User.retrieve_by_token(token_cookie.value).id == user.id


@pytest.mark.usefixtures('user')
def test_login_returns_logged_in_cookie(client):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    cookie = response.cookies['logged_in']

    assert cookie.name == 'logged_in'
    assert not cookie.http_only
    assert cookie.secure
    assert cookie.path == '/'


@pytest.mark.freeze_time('2018-01-01 12:00')
@pytest.mark.usefixtures('user')
@pytest.mark.parametrize('cookie_name', ('access_token', 'logged_in'))
def test_cookies_expiration(cookie_name, config, client):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    cookie = response.cookies[cookie_name]
    expires = datetime.utcfromtimestamp(cookie.max_age)
    delta = config['ACCESS_TOKEN_EXPIRES']

    assert expires - delta == datetime.utcnow()


@pytest.mark.usefixtures('user')
def test_cookies_expiration_synchronous(config, client):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    access_cookie = response.cookies['access_token']
    logged_in_cookie = response.cookies['logged_in']

    assert access_cookie.max_age == logged_in_cookie.max_age


@pytest.mark.usefixtures('user')
def test_login_response_media(client):
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
