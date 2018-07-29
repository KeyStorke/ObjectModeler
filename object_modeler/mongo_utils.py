class ObjectId:
    def __init__(self, value):
        self.id = str(value)

    def __call__(self, *args, **kwargs):
        return self.id


def object_id_serializer(value):
    return str(value)
