from yafas.base import DataApi

from . import models, schemas


class UserApi(DataApi):
    model = models.User
    serializers = {
        'retrieve': schemas.UserInfoSchema(),
    }
