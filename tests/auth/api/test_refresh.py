import pytest
from freezegun import freeze_time

pytestmark = pytest.mark.usefixtures('db')


URL = '/api/v1/auth/refresh/'


def test_success_refresh(client, factory):
    user = factory.user(email='test@test.com', password='test')
    access_token = user.create_access_token()
    refresh_token = user.create_refresh_token()

    got = client.api.post(URL, headers={
        'Authorization': f'Bearer {refresh_token}'})

    assert got['refresh_token'] != refresh_token
    assert got['access_token'] != access_token


def test_with_access_token(client, factory):
    user = factory.user(email='test@test.com', password='test')
    access_token = user.create_access_token()

    response = client.api.post(URL, headers={
        'Authorization': f'Bearer {access_token}'}, as_response=True)

    assert response.status_code == 422
    assert response.json == {
        'message': ['Only refresh tokens can access this endpoint']}


@pytest.mark.parametrize('refresh_token', [
    'lol.kek.makarek.cho',
    'lolkekmakarek',
])
def test_with_invalid_token(refresh_token, client):
    response = client.api.post(URL, headers={
        'Authorization': f'Bearer {refresh_token}'}, as_response=True)

    assert response.status_code == 422


def test_with_expired_refresh_token(client, factory):
    with freeze_time('2018-01-15'):
        user = factory.user(email='test@test.com', password='test')
        refresh_token = user.create_refresh_token()

    with freeze_time('2018-02-25'):
        response = client.api.post(URL, headers={
            'Authorization': f'Bearer {refresh_token}'}, as_response=True)

    assert response.status_code == 401
    assert response.json == {'message': ['Token has expired.']}


def test_options_works(client):
    client.api.options(URL)
