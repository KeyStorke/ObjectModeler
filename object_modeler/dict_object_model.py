from object_modeler.common import check_for_instance, contain_none, contain_str_type, convert_type, is_empty_string, is_last_element, \
    ObjectModelDictMetaclass, PrettyObjectModelDictMetaclass


class _PrototypeDictObjectModel(object):
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
            if item not in self._fields_types.keys():
                raise TypeError('Unknown type for {}'.format(item))
            if self._item_not_found(item, kwargs):
                raise ValueError('required field {}'.format(item))
            if self._optional_item_not_found(item, kwargs):
                continue
            value = kwargs.get(item, self._default_values.get(item))
            self._set_item(item, value)

    def to_dict(self):
        return self.__dict__

    def _item_not_found(self, item, kwargs):
        return item not in kwargs and item not in self._default_values and item not in self._optional_fields

    def _optional_item_not_found(self, item, kwargs):
        return item in self._optional_fields and item not in kwargs and item not in self._default_values

    def _set_item(self, key, value):
        var_types = self._fields_types[key]

        # if value is None
        if value is None and None in var_types:
            setattr(self, key, value)
            return

        if is_empty_string(value) and contain_none(var_types):
            setattr(self, key, None)
            return

        if is_empty_string(value) and contain_str_type(var_types):
            setattr(self, key, "")
            return

        for ordinal, var_type in enumerate(var_types):

            if check_for_instance(var_type, value):
                setattr(self, key, value)
                return

            value, err = convert_type(var_type, value)

            if not err:
                setattr(self, key, value)
                return

            if not is_last_element(ordinal, var_types):
                continue

            types = [str(vtype) for vtype in var_types]
            types = ' or '.join(types)
            raise TypeError(
                '`{}` must be type {}, got {} (`{}`) \n last err: {}'.format(key, types, type(value).__name__, value,
                                                                             err)
            )


class GenericDictObjectModel(_PrototypeDictObjectModel):
    __metaclass__ = ObjectModelDictMetaclass
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()


class PrettyDictObjectModel(_PrototypeDictObjectModel):
    __metaclass__ = PrettyObjectModelDictMetaclass
    all_fields = tuple()
    optional_fields = tuple()
    default_values = dict()
    fields_types = dict()

    def __init__(self, data):
        self.init_model(data)