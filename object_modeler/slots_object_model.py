from object_modeler.common import ObjectModelSlotsMetaclass, _ObjectModel


class _PrototypeSlotsObjectModel(_ObjectModel):
    __slots__ = tuple()
    _all_fields = __slots__
    _fields_types = dict()
    _default_values = dict()
    _optional_fields = dict()

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


class GenericSlotsObjectModel(_PrototypeSlotsObjectModel, metaclass=ObjectModelSlotsMetaclass):
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()
