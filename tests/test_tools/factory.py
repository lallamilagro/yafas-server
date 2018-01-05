from faker import Faker
from flask_sqlalchemy import SQLAlchemy

from yafas.auth.models import User
from yafas.beta.models import BetaUser


def _transaction(method):

    def _decorator(self, *args, **kwargs):
        self.db.session.begin_nested()

        instance = method(self, *args, **kwargs)

        self.db.session.add(instance)
        self.db.session.commit()

        return instance

    return _decorator


class Factory:

    faker = Faker()

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def cycle(self, count: int) -> 'Factory':
        return CycleFactory(self.db, count)

    @_transaction
    def user(self, email: str=None, password: str=None, **kwargs) -> User:
        model = BetaUser if kwargs.pop('beta', False) else User

        return model(
            email=email or self.faker.email(),
            password=password or self.faker.password(), **kwargs)


class CycleFactory:

    def __init__(self, db: SQLAlchemy, count: int) -> Factory:
        self.db = db
        self.count = count

        self.factory = Factory(self.db)

    def __getattr__(self, method_name: str):
        method = getattr(self.factory, method_name)
        return lambda *args, **kwargs: [
            method(*args, **kwargs) for _ in range(self.count)]
