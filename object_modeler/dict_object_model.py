from object_modeler.common import ObjectModelDictMetaclass, PrettyObjectModelDictMetaclass, BaseObjectModel, \
    with_metaclass


class _PrototypeDictObjectModel(BaseObjectModel):
    """ Define a representation dict-based models """

    def __repr__(self):
        return str(self.to_dict())

    def __name__(self):
        return type(self).__name__

    def to_dict(self):
        return self.__dict__


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


class ObjectModel(with_metaclass(PrettyObjectModelDictMetaclass, _PrototypeDictObjectModel)):
    """ Pretty object model """

    def __init__(self, data):
        self.init_model(data)
