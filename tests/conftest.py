import pytest

from tests import Factory


@pytest.fixture
def factory(db):
    return Factory(db)
