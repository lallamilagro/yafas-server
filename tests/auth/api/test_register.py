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

    assert User.retrieve_by_token(token_cookie.value) == User.query.first()


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
