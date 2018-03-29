from marshmallow import fields

from yafas.base import StrictSchema


class TransactionSchema(StrictSchema):
    created_at = fields.DateTime(required=True)
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    value = fields.Float(required=True)
