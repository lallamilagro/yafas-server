import pytest

from yafas.auth.models import User


@pytest.fixture
def user(db):
    user = User(email='test@test.com', password='test')
    db.session.add(user)
    db.session.commit()
    return user
