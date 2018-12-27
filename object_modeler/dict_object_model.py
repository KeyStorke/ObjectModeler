from object_modeler.common import ObjectModelDictMetaclass, PrettyObjectModelDictMetaclass, BaseObjectModel, \
    with_metaclass, get_public_fields_as_dict


class _PrototypeDictObjectModel(BaseObjectModel):
    """ Define a representation dict-based models """

    def __repr__(self):
        return str(self.to_dict())

    def __name__(self):
        return type(self).__name__

    def to_dict(self, excluded_fields=None):

        if excluded_fields is None:
            excluded_fields = set()

        as_dict = get_public_fields_as_dict(self.__dict__, self._hidden_fields, excluded_fields)

        must_be_serialized = ((key, self._serializers[key]) for key in as_dict if key in self._serializers)

        for key, serializer in must_be_serialized:
            as_dict[key] = serializer(as_dict[key])

        return as_dict


class GenericDictObjectModel(with_metaclass(ObjectModelDictMetaclass, _PrototypeDictObjectModel)):
    """ Standard model

    all_fields - tuple of all fields names
    optional_fields - tuple of optional (not required fields names)
    default_values - dict of default values for fields (if value not received in init)
    fields_types - dict of all fields types
    """
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()
    hidden_fields = tuple()


class ObjectModel(with_metaclass(PrettyObjectModelDictMetaclass, _PrototypeDictObjectModel)):
    """ Pretty object model """

    def __init__(self, data):
        self.init_model(data)
