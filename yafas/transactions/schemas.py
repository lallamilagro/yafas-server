from marshmallow import fields, post_load

from yafas import db
from yafas.base import StrictSchema

from .models import Transaction


class BaseSchema(StrictSchema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)

    def transaction(self, **kwargs) -> Transaction:
        return Transaction.query.get_by(**kwargs)


class TransactionSchema(StrictSchema):
    created_at = fields.DateTime(required=True)
    id = fields.Int(required=True)
    value = fields.Float(required=True)


class TransactionRetrieveSchema(BaseSchema):

    @post_load
    def retrieve(self, data: dict) -> Transaction:
        instance = self.transaction(**data)
        return TransactionSchema().dump(instance)[0]


class TransactionUpdateSchema(BaseSchema):
    value = fields.Decimal(required=True)

    @post_load
    def update(self, data: dict) -> dict:
        value = data.pop('value')

        instance = self.transaction(**data)

        instance.value = value
        db.session.add(instance)
        db.session.commit()

        return TransactionSchema().dump(instance)[0]


class TransactionDeleteSchema(BaseSchema):

    @post_load
    def delete(self, data: dict):
        instance = self.transaction(**data)

        db.session.delete(instance)
        db.session.commit()


class TransactionCreateSchema(StrictSchema):
    value = fields.Decimal(required=True)
    user_id = fields.Int(required=True)

    @post_load
    def create(self, data: dict) -> dict:
        instance = Transaction(**data)
        db.session.add(instance)
        db.session.commit()

        return TransactionSchema().dump(instance)[0]


class TransactionListSchema(StrictSchema):
    user_id = fields.Int(required=True)

    @post_load
    def list(self, data: dict) -> list:
        instances = Transaction.query.filter_by(**data)
        return TransactionSchema(many=True).dump(instances)[0]
