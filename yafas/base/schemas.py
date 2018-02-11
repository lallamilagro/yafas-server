from marshmallow import Schema


class StrictSchema(Schema):

    def __init__(self, *args, **kwargs):
        kwargs['strict'] = True
        return super().__init__(*args, **kwargs)
