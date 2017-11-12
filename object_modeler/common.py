def check_for_instance(var_type, var):
    """ checking an instance of

    :param var_type: any type
    :param var: any object
    :return: check result
    """
    return isinstance(var_type, type) and isinstance(var, var_type)


def is_last_element(ordinal, lst):
    """ checking whether an last element of list

    :param ordinal: ordinal element in list
    :param lst: list
    :return: check result
    """
    return ordinal + 1 == len(lst)


def convert_type(var_type, var):
    """ convert value to type

    :param var_type: type for convert
    :param var: value for convert
    :return: converting result and exception/None
    """
    try:
        value = var_type(var)
        return value, None
    except Exception as e:
        import traceback as tb
        tb.print_exc()

        return var, e


def contain_str_type(lst):
    """ check contain str in list

    :param lst: list for checking
    :return: check result
    """
    return str in lst


def contain_none(lst):
    """ check contain None in list

    :type lst: list for checking
    :return: check result
    """
    return None in lst


def is_empty_string(var):
    """ check for empty string

    :param var:
    :return: check result
    """
    return not var and isinstance(var, str)


def compare_lists(lst, other_lst):
    """ compare two lists

    :param lst: list for compare
    :param other_lst: list for compare
    :return: result compare
    """
    return sorted(lst) == sorted(other_lst)


def contain_all_elements(lst, other_lst):
    """ checking whether the second contains a list of all the elements of the first

    :param lst: first list
    :param other_lst: second list
    :return: check result
    """
    for i in other_lst:
        if i not in lst:
            return False
    return True


def is_correct_datatypes(datatypes):
    """ check list of data types for correct

    :param datatypes: list of data types
    :return: check result
    """
    if not datatypes:
        return True

    flatten = lambda l: [item for sublist in l for item in sublist]
    _datatypes = flatten(datatypes)
    return all(map(lambda datatype: callable(datatype) or datatype is None, _datatypes))


def check_for_empty_values(dictionary):
    return all(dictionary.values())


def checking_cls_dictionary(cls_dict):
    # for all fields must be defined data type
    assert compare_lists(cls_dict.get('all_fields', tuple()), cls_dict.get('fields_types', dict()).keys())

    # check for empty types
    assert check_for_empty_values(cls_dict.get('fields_types', dict()))

    # all fields must be defined in all_fields
    assert contain_all_elements(cls_dict.get('all_fields', tuple()), cls_dict.get('optional_fields', tuple()))
    assert contain_all_elements(cls_dict.get('all_fields', tuple()), cls_dict.get('default_values', dict()).keys())


def new_slots_class(mcs, name, bases, cls_dict):
    checking_cls_dictionary(cls_dict)

    cls_dict['__slots__'] = cls_dict.get('all_fields', tuple())
    cls_dict['_all_fields'] = cls_dict.get('all_fields', tuple())
    cls_dict['_optional_fields'] = cls_dict.get('optional_fields', tuple())
    cls_dict['_default_values'] = cls_dict.get('default_values', dict())
    cls_dict['_fields_types'] = cls_dict.get('fields_types', dict())

    # conflicts __slots__ with class vars
    for item in cls_dict['all_fields']:
        cls_dict.pop(item, None)

    cls_dict.pop('all_fields', None)
    cls_dict.pop('optional_fields', None)
    cls_dict.pop('default_values', None)
    cls_dict.pop('fields_types', None)

    return type.__new__(mcs, name, bases, cls_dict)


def new_dict_class(mcs, name, bases, cls_dict):
    checking_cls_dictionary(cls_dict)
    cls_dict['_all_fields'] = cls_dict.get('all_fields', tuple())
    cls_dict['_optional_fields'] = cls_dict.get('optional_fields', tuple())
    cls_dict['_default_values'] = cls_dict.get('default_values', dict())
    cls_dict['_fields_types'] = cls_dict.get('fields_types', dict())

    cls_dict.pop('all_fields', None)
    cls_dict.pop('optional_fields', None)
    cls_dict.pop('default_values', None)
    cls_dict.pop('fields_types', None)

    return type.__new__(mcs, name, bases, cls_dict)


class Undefined(object): pass


class ObjectModel(object):
    __slots__ = tuple()
    _all_fields = tuple()
    _fields_types = dict()
    _default_values = dict()
    _optional_fields = dict()

    def init_model(self, kwargs):
        for item in self._all_fields:
            if item not in kwargs and item not in self._default_values and item not in self._optional_fields:
                raise ValueError('required field {}'.format(item))

            if item in kwargs:
                value = kwargs.get(item)
            else:
                value = self._default_values.get(item)

            self._set_item(item, value)

    def _set_item(self, key, value):

        # if value is None
        if type(value) in self._fields_types[key] or (value is None and value in self._fields_types[key]):
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

            if callable(var_type):
                value, err = convert_type(var_type, value)

                if not err:
                    setattr(self, key, value)
                    return

        types = [str(vtype) for vtype in var_types]
        types = ' or '.join(types)
        raise TypeError(
            '`{}` must be type {}, got {} (`{}`) \n last err: {}\n types: {}'.format(key, types, type(value).__name__, value,
                                                                         err, var_types)
        )


class ObjectModelSlotsMetaclass(type):
    def __new__(mcs, name, bases, cls_dict):
        return new_slots_class(mcs, name, bases, cls_dict)


class ObjectModelDictMetaclass(type):
    def __new__(mcs, name, bases, cls_dict):
        return new_dict_class(mcs, name, bases, cls_dict)


class Field(object):
    def __init__(self, types=None, optional=False, default_value=Undefined()):
        if types is not None:
            self.type_list = types
        else:
            self.type_list = list()

        self.optional = optional
        self.default_value = default_value

    def types(self, *args):
        self.type_list += args
        return self


class PrettyObjectModelDictMetaclass(type):
    def __new__(mcs, name, bases, cls_dict):
        items = list()

        all_fields = list()
        optional_fields = list()
        default_values = dict()
        fields_types = dict()

        for base_class in bases:
            if hasattr(base_class, '_all_fields'):
                all_fields += getattr(base_class, '_all_fields')
                optional_fields += getattr(base_class, '_optional_fields')
                fields_types.update(getattr(base_class, '_fields_types'))
                default_values.update(getattr(base_class, '_default_values'))

        for field_name, value in cls_dict.items():

            if isinstance(value, Field):
                items.append((field_name, value))

        for field_name, field in items:
            all_fields.append(field_name)
            if field.optional:
                optional_fields.append(field_name)

            if not isinstance(field.default_value, Undefined):
                default_values[field_name] = field.default_value

            fields_types[field_name] = field.type_list

        cls_dict['all_fields'] = tuple(set(all_fields))
        cls_dict['optional_fields'] = tuple(set(optional_fields))
        cls_dict['default_values'] = default_values
        cls_dict['fields_types'] = fields_types

        return new_dict_class(mcs, name, bases, cls_dict)


class PrettyObjectModelSlotsMetaclass(type):
    def __new__(mcs, name, bases, cls_dict):
        items = list()

        all_fields = list()
        optional_fields = list()
        default_values = dict()
        fields_types = dict()

        for base_class in bases:
            if hasattr(base_class, '_all_fields'):
                all_fields += getattr(base_class, '_all_fields')
                optional_fields += getattr(base_class, '_optional_fields')
                fields_types.update(getattr(base_class, '_fields_types'))
                default_values.update(getattr(base_class, '_default_values'))

        for field_name, value in cls_dict.items():

            if isinstance(value, Field):
                items.append((field_name, value))

        for field_name, field in items:
            all_fields.append(field_name)
            if field.optional:
                optional_fields.append(field_name)

            if not isinstance(field.default_value, Undefined):
                default_values[field_name] = field.default_value

            fields_types[field_name] = field.type_list

        cls_dict['__slots__'] = tuple(set(all_fields))
        cls_dict['all_fields'] = tuple(set(all_fields))
        cls_dict['optional_fields'] = tuple(set(optional_fields))
        cls_dict['default_values'] = default_values
        cls_dict['fields_types'] = fields_types

        return new_slots_class(mcs, name, bases, cls_dict)
