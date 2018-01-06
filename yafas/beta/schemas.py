from marshmallow import fields, post_load

from yafas import db
from yafas.auth.schemas import EmailSchema

from .models import BetaUser


class RegistrationSchema(EmailSchema):
    password = fields.Str(required=True)

    @post_load
    def create_beta_user(self, data) -> BetaUser:
        beta = BetaUser(**data)
        db.session.add(beta)
        db.session.commit()
        return beta
