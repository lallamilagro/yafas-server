import pytest


@pytest.fixture
def user_and_transaction(factory):
    def make(**kwargs):
        user = factory.user()
        return user, factory.transaction(user_id=user.id, **kwargs)
    return make
