from datetime import datetime

import pytest

from tests import cors_callback
from yafas.auth.models import User

pytestmark = pytest.mark.client(callback=cors_callback)

URL = '/api/v1/auth/register/'


def test_registration_creates_user(client):
    client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    })

    assert User.query.filter_by(email='test@test.com').first()


def test_registration_returns_cookie_token(client):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    token_cookie = response.cookies['access_token']

    assert token_cookie.name == 'access_token'
    assert token_cookie.http_only
    assert token_cookie.secure
    assert token_cookie.path == '/'

    assert User.retrieve_by_token(token_cookie.value) == User.query.first()


def test_registration_returns_logged_in_cookie(client):
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


def test_cookies_expiration_synchronous(config, client):
    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    access_cookie = response.cookies['access_token']
    logged_in_cookie = response.cookies['logged_in']

    assert access_cookie.max_age == logged_in_cookie.max_age


def test_registration_response_media(client):
    got = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    })

    assert got == {}


def test_failed_when_password_incorrect(client):
    response = client.post(URL, json={
        'email': 'test.com',
        'password': 'test',
    }, as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['Not a valid email address.']}
    assert not response.cookies

    assert not User.query.first()


@pytest.mark.parametrize('data, error', (
    (
        {'email': 'test@test.com'},
        {'password': ['Missing data for required field.']},
    ), (
        {'password': 'test'},
        {'email': ['Missing data for required field.']},
    ), (
        {},
        {'password': ['Missing data for required field.'],
         'email': ['Missing data for required field.']},
    ),
))
def test_failed_when_required_fields_skipped(data, error, client):
    response = client.post(URL, json=data, as_response=True)

    assert response.status_code == 400
    assert response.json == error
    assert not response.cookies

    assert not User.query.first()


def test_failed_if_already_registered(client, factory):
    factory.user(email='test@test.com')

    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['This email is already in use.']}
    assert not response.cookies


def test_options_works(client):
    client.options(URL)
