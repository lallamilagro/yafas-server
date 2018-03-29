from decimal import Decimal
from typing import Union

from faker import Faker

from yafas import db
from yafas.auth.models import User
from yafas.transactions.models import Transaction


def _transaction(method):

    def _decorator(self, *args, **kwargs):
        instance = method(self, *args, **kwargs)

        db.session.add(instance)
        db.session.flush()
        # refresh instance for real database representation
        db.session.refresh(instance)

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

    @_transaction
    def transaction(
            self,
            value: Union[int, float, Decimal] = None,
            user_id: int = None) -> Transaction:
        return Transaction(
            value=value or self.faker.random_number(digits=6),
            user_id=user_id or self.user().id,
        )


class CycleFactory:

    def __init__(self, count: int) -> Factory:
        self.count = count

        self.factory = Factory()

    def __getattr__(self, method_name: str):
        method = getattr(self.factory, method_name)
        return lambda *args, **kwargs: [
            method(*args, **kwargs) for _ in range(self.count)]
