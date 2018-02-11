from faker import Faker

from yafas import db
from yafas.auth.models import User


def _transaction(method):

    def _decorator(self, *args, **kwargs):
        db.session.begin_nested()

        instance = method(self, *args, **kwargs)

        db.session.add(instance)
        db.session.commit()

        return instance

    return _decorator


class Factory:

    faker = Faker()

    def cycle(self, count: int) -> 'Factory':
        return CycleFactory(count)

    @_transaction
    def user(self, email: str=None, password: str=None, **kwargs) -> User:
        return User(
            email=email or self.faker.email(),
            password=password or self.faker.password(), **kwargs)


class CycleFactory:

    def __init__(self, count: int) -> Factory:
        self.count = count

        self.factory = Factory()

    def __getattr__(self, method_name: str):
        method = getattr(self.factory, method_name)
        return lambda *args, **kwargs: [
            method(*args, **kwargs) for _ in range(self.count)]
