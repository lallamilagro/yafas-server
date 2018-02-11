import pytest

from yafas.auth.models import User

pytestmark = pytest.mark.usefixtures('db')

URL = '/api/v1/auth/register/'


def test_success(client, db):
    client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    })

    assert db.session.query(User).filter_by(email='test@test.com').first()


def test_failed_when_password_incorrect(client, db):
    response = client.post(URL, json={
        'email': 'test.com',
        'password': 'test',
    }, as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['Not a valid email address.']}

    assert not db.session.query(User).first()


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
def test_failed_when_required_fields_skipped(data, error, client, db):
    response = client.post(URL, json=data, as_response=True)

    assert response.status_code == 400
    assert response.json == error

    assert not db.session.query(User).first()


def test_failed_if_already_registered(client, factory):
    factory.user(email='test@test.com')

    response = client.post(URL, json={
        'email': 'test@test.com',
        'password': 'test',
    }, as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['This email is already in use.']}


def test_options_works(client):
    client.options(URL)
