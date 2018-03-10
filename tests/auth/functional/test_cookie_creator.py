import pytest

from yafas.auth import CookieCreator
from yafas.auth.models import User


@pytest.fixture
def cookies_data(factory):
    user = factory.user()
    creator = CookieCreator(user.create_access_token())
    return creator()


def test_expiration_synchronous(cookies_data):
    access_cookie = cookies_data['access_token']
    logged_in = cookies_data['logged_in']

    assert access_cookie['max_age'] == logged_in['max_age']


def test_cookies_are_secure(cookies_data):
    access_cookie = cookies_data['access_token']
    logged_in = cookies_data['logged_in']

    assert access_cookie['secure'] == logged_in['secure']
    assert access_cookie['secure'] is True


def test_cookies_has_domain(cookies_data):
    access_cookie = cookies_data['access_token']
    logged_in = cookies_data['logged_in']

    assert access_cookie['domain'] == logged_in['domain']
    assert access_cookie['domain'] == 'yafas.org'


def test_access_cookie_is_http_only(cookies_data):
    access_cookie = cookies_data['access_token']

    assert access_cookie['http_only']


def test_logged_in_cookie_is_not_http_only(cookies_data):
    logged_in = cookies_data['logged_in']

    assert not logged_in['http_only']


def test_access_cookie_has_a_token(cookies_data):
    access_cookie = cookies_data['access_token']

    assert User.retrieve_by_token(access_cookie['value'])
