from object_modeler.common import contain_none, contain_str_type, convert_type, is_empty_string, \
    ObjectModelDictMetaclass, PrettyObjectModelDictMetaclass


class _PrototypeDictObjectModel:
    _all_fields = tuple()
    _fields_types = dict()
    _default_values = dict()
    _optional_fields = dict()

    def __repr__(self):
        return str(self.to_dict())

    def __name__(self):
        return type(self).__name__

    def init_model(self, kwargs):
        for item in self._all_fields:
            if item not in kwargs and item not in self._default_values and item not in self._optional_fields:
                raise ValueError('required field {}'.format(item))

            if item in kwargs:
                value = kwargs.get(item)
            else:
                value = self._default_values.get(item)

            self._set_item(item, value)

    def to_dict(self):
        return self.__dict__

    def _set_item(self, key, value):

        # if value is None
        if type(value) in self._fields_types[key]:
            setattr(self, key, value)
            return

        var_types = self._fields_types[key]

        if is_empty_string(value):

            if contain_none(var_types):
                setattr(self, key, None)
                return

            if contain_str_type(var_types):
                setattr(self, key, "")
                return

        err = None

        for var_type in var_types:

            value, err = convert_type(var_type, value)

            if not err:
                setattr(self, key, value)
                return

        types = [str(vtype) for vtype in var_types]
        types = ' or '.join(types)
        raise TypeError(
            '`{}` must be type {}, got {} (`{}`) \n last err: {}'.format(key, types, type(value).__name__, value,
                                                                         err)
        )


class GenericDictObjectModel(_PrototypeDictObjectModel, metaclass=ObjectModelDictMetaclass):
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()


class PrettyDictObjectModel(_PrototypeDictObjectModel, metaclass=PrettyObjectModelDictMetaclass):
    def __init__(self, data):
        self.init_model(data)
