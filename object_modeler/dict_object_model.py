from object_modeler.common import ObjectModelDictMetaclass, PrettyObjectModelDictMetaclass, ObjectModel
from six import with_metaclass


class _PrototypeDictObjectModel(ObjectModel):
    def __repr__(self):
        return str(self.to_dict())

    def __name__(self):
        return type(self).__name__

    def to_dict(self):
        return self.__dict__


class GenericDictObjectModel(with_metaclass(ObjectModelDictMetaclass, _PrototypeDictObjectModel)):
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()


class PrettyDictObjectModel(with_metaclass(PrettyObjectModelDictMetaclass, _PrototypeDictObjectModel)):

    def __init__(self, data):
        self.init_model(data)
