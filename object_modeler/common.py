from typing import List, Tuple


class Undefined: pass


class ObjectModel:
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


def check_for_instance(var_type: type or None, var: object) -> bool:
    """ checking an instance of

    :param var_type: any type
    :param var: any object
    :return: check result
    """
    return isinstance(var_type, type) and isinstance(var, var_type)


def is_last_element(ordinal: int, lst: list) -> bool:
    """ checking whether an last element of list

    :param ordinal: ordinal element in list
    :param lst: list
    :return: check result
    """
    return ordinal + 1 == len(lst)


def convert_type(var_type: type, var: object) -> (object, Exception):
    """ convert value to type

    :param var_type: type for convert
    :param var: value for convert
    :return: converting result and exception/None
    """
    try:
        value = var_type(var)
        return value, None
    except Exception as e:
        return var, e


def contain_str_type(lst: list) -> bool:
    """ check contain str in list

    :param lst: list for checking
    :return: check result
    """
    return str in lst


def contain_none(lst: list) -> bool:
    """ check contain None in list

    :type lst: list for checking
    :return: check result
    """
    return None in lst


def is_empty_string(var: object) -> bool:
    """ check for empty string

    :param var:
    :return: check result
    """
    return not var and isinstance(var, str)


def compare_lists(lst: list, other_lst: list) -> bool:
    """ compare two lists

    :param lst: list for compare
    :param other_lst: list for compare
    :return: result compare
    """
    return sorted(lst) == sorted(other_lst)


def contain_all_elements(lst: list, other_lst: list) -> bool:
    """ checking whether the second contains a list of all the elements of the first

    :param lst: first list
    :param other_lst: second list
    :return: check result
    """
    for i in other_lst:
        if i not in lst:
            return False
    return True


def is_correct_datatypes(datatypes: List[Tuple]) -> bool:
    """ check list of data types for correct

    :param datatypes: list of data types
    :return: check result
    """
    if not datatypes:
        return True

    flatten = lambda l: [item for sublist in l for item in sublist]
    _datatypes = flatten(datatypes)
    return all(map(lambda datatype: callable(datatype) or datatype is None, _datatypes))


def checking_cls_dictionary(cls_dict):
    # for all fields must be defined data type
    assert compare_lists(cls_dict['all_fields'], cls_dict['fields_types'].keys())

    # all fields must be defined in all_fields
    assert contain_all_elements(cls_dict['all_fields'], cls_dict['optional_fields'])
    assert contain_all_elements(cls_dict['all_fields'], cls_dict['default_values'].keys())


def new_slots_class(mcs, name, bases, cls_dict):
    checking_cls_dictionary(cls_dict)

    cls_dict['__slots__'] = cls_dict['all_fields']
    cls_dict['_all_fields'] = cls_dict['all_fields']
    cls_dict['_optional_fields'] = cls_dict['optional_fields']
    cls_dict['_default_values'] = cls_dict['default_values']
    cls_dict['_fields_types'] = cls_dict['fields_types']

    # conflicts __slots__ with class vars
    for item in cls_dict['all_fields']:
        cls_dict.pop(item, None)

    cls_dict.pop('all_fields')
    cls_dict.pop('optional_fields')
    cls_dict.pop('default_values')
    cls_dict.pop('fields_types')

    return type.__new__(mcs, name, bases, cls_dict)


def new_dict_class(mcs, name, bases, cls_dict: dict):
    checking_cls_dictionary(cls_dict)

    cls_dict['_all_fields'] = cls_dict['all_fields']
    cls_dict['_optional_fields'] = cls_dict['optional_fields']
    cls_dict['_default_values'] = cls_dict['default_values']
    cls_dict['_fields_types'] = cls_dict['fields_types']

    cls_dict.pop('all_fields')
    cls_dict.pop('optional_fields')
    cls_dict.pop('default_values')
    cls_dict.pop('fields_types')

    return type.__new__(mcs, name, bases, cls_dict)


class ObjectModelSlotsMetaclass(type):
    def __new__(mcs, name, bases, cls_dict: dict):
        return new_slots_class(mcs, name, bases, cls_dict)


class ObjectModelDictMetaclass(type):
    def __new__(mcs, name, bases, cls_dict: dict):
        return new_dict_class(mcs, name, bases, cls_dict)


class Field:
    def __init__(self, types: tuple, optional: bool = False, default_value: object = Undefined()):
        self.types = types
        self.optional = optional
        self.default_value = default_value


class PrettyObjectModelDictMetaclass(type):
    def __new__(mcs, name, bases, cls_dict: dict):
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

            fields_types[field_name] = field.types

        cls_dict['all_fields'] = tuple(set(all_fields))
        cls_dict['optional_fields'] = tuple(set(optional_fields))
        cls_dict['default_values'] = default_values
        cls_dict['fields_types'] = fields_types

        return new_dict_class(mcs, name, bases, cls_dict)


class PrettyObjectModelSlotsMetaclass(type):
    def __new__(mcs, name, bases, cls_dict: dict):
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

            fields_types[field_name] = field.types

        cls_dict['__slots__'] = tuple(set(all_fields))
        cls_dict['all_fields'] = tuple(set(all_fields))
        cls_dict['optional_fields'] = tuple(set(optional_fields))
        cls_dict['default_values'] = default_values
        cls_dict['fields_types'] = fields_types

        return new_slots_class(mcs, name, bases, cls_dict)
