from yafas.base import DataApi

from . import models, schemas


class TransactionApi(DataApi):

    model = models.Transaction
    serializers = {
        'retrieve': schemas.TransactionSchema(),
        'create': schemas.TransactionCreateSchema(),
        'update': schemas.TransactionCreateSchema(),
    }
