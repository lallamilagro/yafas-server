from marshmallow import fields

from yafas.base import StrictSchema


class TransactionSchema(StrictSchema):
    on_date = fields.DateTime(required=True)
    id = fields.Int(required=True)
    value = fields.Float(required=True)


class TransactionCreateSchema(StrictSchema):
    value = fields.Decimal(required=True)
    on_date = fields.DateTime(required=False)
