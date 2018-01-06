import pytest

from yafas.auth.models import User

pytestmark = pytest.mark.usefixtures('db')


def url(email: str) -> str:
    return f'/api/v1/auth/check-email/{email}/'


def test_is_free(client, factory):
    factory.user(email='test@test.com')

    client.api.get(url('test-user@test.com'))

    assert User.query.count() == 1


def test_already_used(client, factory):
    factory.user(email='test@test.com')

    response = client.api.get(url('test@test.com'), as_response=True)

    assert response.status_code == 400
    assert User.query.count() == 1


def test_invalid_email(client):
    response = client.api.get(url('test'), as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['Not a valid email address.']}
