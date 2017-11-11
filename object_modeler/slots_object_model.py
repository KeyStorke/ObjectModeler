from object_modeler.common import ObjectModelSlotsMetaclass, ObjectModel, PrettyObjectModelSlotsMetaclass
from six import with_metaclass


class _PrototypeSlotsObjectModel(ObjectModel):
    __slots__ = tuple()

    def __repr__(self):
        return str(self.to_dict())

    def __name__(self):
        return type(self).__name__

    def to_dict(self):
        result = dict()
        for item in self._all_fields:
            if hasattr(self, item):
                result[item] = getattr(self, item)
            elif item in self._optional_fields:
                continue
            else:
                raise AttributeError('{} object has no attribute {}'.format(self.__name__, item))
        return result


class GenericSlotsObjectModel(with_metaclass(ObjectModelSlotsMetaclass, _PrototypeSlotsObjectModel)):
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()


class PrettySlotsObjectModel(with_metaclass(PrettyObjectModelSlotsMetaclass, _PrototypeSlotsObjectModel)):
    __slots__ = tuple()

    def __init__(self, data):
        self.init_model(data)
