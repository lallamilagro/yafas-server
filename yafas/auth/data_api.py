from yafas.base.data_api import DataApi

from . import models, schemas


class UserApi(DataApi):
    model = models.User
    serializers = {
        'retrieve': schemas.UserInfoSchema(),
    }
