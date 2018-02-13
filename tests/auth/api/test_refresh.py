import pytest

from tests import cors_callback

pytestmark = pytest.mark.client(callback=cors_callback)

URL = '/api/v1/auth/refresh/'


@pytest.mark.freeze_time('2018-01-01 12:00')
def test_success_refresh(freezer, client, factory):
    user = factory.user(email='test@test.com', password='test')

    access_token = user.create_access_token()
    refresh_token = user.create_refresh_token()

    freezer.move_to('2018-01-01 12:01')
    got = client.post(URL, headers={
        'Authorization': f'Bearer {refresh_token}'})

    assert got['refresh_token'] != refresh_token
    assert got['access_token'] != access_token


def test_with_access_token(client, factory):
    user = factory.user(email='test@test.com', password='test')
    access_token = user.create_access_token()

    response = client.post(URL, headers={
        'Authorization': f'Bearer {access_token}'}, as_response=True)

    assert response.status_code == 422
    assert response.json == {
        'message': ['Only refresh tokens can access this endpoint']}


@pytest.mark.parametrize('refresh_token', [
    'lol.kek.makarek.cho',
    'lolkekmakarek',
])
def test_with_invalid_token(refresh_token, client):
    response = client.post(URL, headers={
        'Authorization': f'Bearer {refresh_token}'}, as_response=True)

    assert response.status_code == 422


def test_with_expired_refresh_token(freezer, client, factory):
    freezer.move_to('2018-01-15')
    user = factory.user(email='test@test.com', password='test')
    refresh_token = user.create_refresh_token()

    freezer.move_to('2018-02-25')
    response = client.post(URL, headers={
        'Authorization': f'Bearer {refresh_token}'}, as_response=True)

    assert response.status_code == 401
    assert response.json == {'message': ['Signature has expired']}


def test_options_works(client):
    client.options(URL)
