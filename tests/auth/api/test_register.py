import pytest

from yafas.auth.models import User

pytestmark = pytest.mark.usefixtures('db')

URL = '/api/v1/auth/register/'


def test_success(client):
    client.api.post(URL, data={
        'email': 'test@test.com',
        'password': 'test',
    })

    assert User.query.filter_by(email='test@test.com').first()


def test_failed_when_password_incorrect(client):
    response = client.api.post(URL, data={
        'email': 'test.com',
        'password': 'test',
    }, as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['Not a valid email address.']}

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
    response = client.api.post(URL, data=data, as_response=True)

    assert response.status_code == 400
    assert response.json == error

    assert not User.query.first()


def test_failed_if_already_registered(client, factory):
    factory.user(email='test@test.com')

    response = client.api.post(URL, data={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['This email is already in use.']}

    assert User.query.count() == 1


def test_options_works(client):
    client.api.options(URL)
