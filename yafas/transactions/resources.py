from . import models, schemas


class Transaction:

    def instance(self, id: int) -> models.Transaction:
        return models.Transaction.query.get_by(
            id=id,
            user_id=self.user().id,
        )

    def on_get(self, request, response, id: int):
        instance = self.instance(id)
        response.media, _ = schemas.TransactionSchema().dump(instance)
