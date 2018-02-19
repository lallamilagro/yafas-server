import pytest

from tests import cors_callback

pytestmark = pytest.mark.client(callback=cors_callback)


def url(email: str) -> str: return f'/api/v1/auth/check-email/{email}/'


def test_is_free(client, factory):
    factory.user(email='test@test.com')

    assert client.get(url('test-user@test.com')) == {}


def test_already_used(client, factory):
    factory.user(email='test@test.com')

    response = client.get(url('test@test.com'), as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['This email is already in use.']}


def test_invalid_email(client):
    response = client.get(url('test'), as_response=True)

    assert response.status_code == 400
    assert response.json == {'email': ['Not a valid email address.']}
