import falcon

from . import schemas


class Transaction:

    def on_get(self, request, response, id: int):
        response.media, _ = schemas.TransactionRetrieveSchema().load(dict(
            id=id, user_id=self.user().id,
        ))

    def on_put(self, request, response, id: int):
        response.media, _ = schemas.TransactionUpdateSchema().load(dict(
            user_id=self.user().id, id=id, **request.media,
        ))

    def on_delete(self, request, response, id: int):
        schemas.TransactionDeleteSchema().load(dict(
            user_id=self.user().id, id=id,
        ))
        response.status = falcon.HTTP_204
