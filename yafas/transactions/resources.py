import falcon

from .data_api import TransactionApi


class Transaction:

    @staticmethod
    def data_api(id, request):
        return TransactionApi(id=id, user_id=request.user_id)

    def on_get(self, request, response, id: int):
        response.media = self.data_api(id, request).retrieve()

    def on_put(self, request, response, id: int):
        response.media = self.data_api(id, request).update(
            **request.media,
        )

    def on_delete(self, request, response, id: int):
        self.data_api(id, request).delete()
        response.status = falcon.HTTP_204


class Transactions:

    @staticmethod
    def data_api(request):
        return TransactionApi(user_id=request.user_id)

    def on_post(self, request, response):
        response.media = self.data_api(request).create(**request.media)
        response.status = falcon.HTTP_201

    def on_get(self, request, response):
        response.media = self.data_api(request).list()
