from object_modeler.common import ObjectModelDictMetaclass, PrettyObjectModelDictMetaclass, ObjectModel


class _PrototypeDictObjectModel(ObjectModel):
    def __repr__(self):
        return str(self.to_dict())

    def __name__(self):
        return type(self).__name__

    def to_dict(self):
        return self.__dict__


class GenericDictObjectModel(_PrototypeDictObjectModel, metaclass=ObjectModelDictMetaclass):
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()


class PrettyDictObjectModel(_PrototypeDictObjectModel, metaclass=PrettyObjectModelDictMetaclass):
    def __init__(self, data):
        self.init_model(data)
