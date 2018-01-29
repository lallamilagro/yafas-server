import pytest

pytestmark = pytest.mark.usefixtures('db')


URL = '/api/v1/auth/login/'


def test_success_login(client, factory):
    factory.user(email='test@test.com', password='test')

    got = client.api.post(URL, data={
        'email': 'test@test.com', 'password': 'test'})

    assert 'access_token' in got
    assert 'refresh_token' in got


@pytest.mark.parametrize('credentials', [
    dict(email='test@test.ru', password='test'),
    dict(email='test@test.com', password='watwatwat'),
])
def test_invalid_credential(credentials, client, factory):
    factory.user(email='test@test.com', password='test')

    response = client.api.post(URL, data=credentials, as_response=True)

    assert response.status_code == 400
    assert response.json == {'message': ['Not a valid credentials.']}


def test_options_works(client):
    client.api.options(URL)