import pytest

from tests import cors_callback

pytestmark = pytest.mark.client(callback=cors_callback)

URL = '/api/v1/auth/info/'


@pytest.mark.freeze_time('2018-01-01 12:00')
def test_response_content(client, factory):
    user = factory.user(email='test@test.com', password='test')
    access_token = user.create_access_token()

    headers = {'cookie': f'access_token={access_token}'}
    got = client.get(URL, headers=headers)

    assert got == {
        'email': 'test@test.com',
        'id': 1,
        'registered_in': '2018-01-01T12:00:00+00:00',
    }


def test_no_tokens_passed(client, factory):
    response = client.get(URL, as_response=True)

    assert response.status_code == 401
    assert response.json == {'message': ['No tokens passed']}


@pytest.mark.parametrize('access_token', [
    'lol.kek.makarek.cho',
    'lolkekmakarek',
])
def test_invalid_token_passed(access_token, client):
    headers = {'cookie': f'access_token={access_token}'}
    response = client.post(URL, headers=headers, as_response=True)

    assert response.status_code == 422


@pytest.mark.freeze_time('2018-01-15')
def test_expired_token_passed(freezer, client, factory):
    user = factory.user(email='test@test.com', password='test')
    access_token = user.create_access_token()
    headers = {'cookie': f'access_token={access_token}'}

    freezer.move_to('2018-02-25')
    response = client.post(URL, headers=headers, as_response=True)

    assert response.status_code == 401
    assert response.json == {'message': ['Signature has expired']}


def test_options_works(client):
    client.options(URL)
