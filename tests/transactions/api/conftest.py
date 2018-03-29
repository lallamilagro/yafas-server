import pytest


@pytest.fixture
def user_and_transaction(factory):
    def make(**kwargs):
        user = factory.user()
        return user, factory.transaction(user_id=user.id, **kwargs)
    return make


@pytest.fixture
def url():
    def make_url(id: int = None) -> str:
        _url = '/api/v1/transactions/'
        return f'{_url}{id}/' if id else _url
    return make_url
