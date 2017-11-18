from six import with_metaclass

from object_modeler.common import ObjectModelSlotsMetaclass, BaseObjectModel, PrettyObjectModelSlotsMetaclass


class _PrototypeSlotsObjectModel(BaseObjectModel):
    """ Define a representation slots-based models """
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
    """ Standard slots-based model """
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()


class SlotsObjectModel(with_metaclass(PrettyObjectModelSlotsMetaclass, _PrototypeSlotsObjectModel)):
    """ Pretty slots-based object model """
    __slots__ = tuple()

    def __init__(self, data):
        self.init_model(data)
