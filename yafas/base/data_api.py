from yafas import db


def serialize(fn):
    def method(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        serializer = self.serializers['retrieve']

        if hasattr(result, '__iter__'):
            return serializer.dump(result, many=True)[0]

        return serializer.dump(result)[0]

    return method


def prepare_data(fn):
    def method(self, *args, **data):
        serializer = self.serializers[fn.__name__]
        data, _ = serializer.load(data)
        return fn(self, *args, **data)
    return method


class DataApi:

    model = None
    serializers = {
        'retrieve': None,
        'create': None,
        'update': None,
    }

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def instance(self):
        return self.model.query.get_by(**self.kwargs)

    @serialize
    def retrieve(self):
        return self.instance()

    @serialize
    @prepare_data
    def update(self, **data):
        instance = self.instance()
        for key, value in data.items():
            setattr(instance, key, value)

        db.session.add(instance)
        db.session.commit()
        return instance

    def delete(self):
        instance = self.instance()
        db.session.delete(instance)
        db.session.commit()

    @serialize
    @prepare_data
    def create(self, **data):
        instance = self.model(**self.kwargs, **data)
        db.session.add(instance)
        db.session.commit()
        return instance

    @serialize
    def list(self, **data):
        return self.model.query.filter_by(**self.kwargs, **data)
