import sys

PY3 = sys.version_info >= (3, 0)


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


def _is_empty_string_py2(var):
    """ check for empty string in python2

    :param var:
    :return: check result
    """
    return (isinstance(var, str) or isinstance(var, unicode)) and not var


def _is_empty_string_py3(var):
    """ check for empty string in python3

    :param var:
    :return: check result
    """
    return isinstance(var, str) and not var


def check_types_list(lst):
    """ check for non callable types

    :param lst: list of types
    :return: check result
    """
    for vartypes in lst:
        for item in vartypes:
            if not callable(item) and item is not None:
                print(item)
                return False
    return True


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


def check_for_empty_values(dictionary):
    """ checking dict for empty values

    :param dictionary: dict for checking
    :return: check result
    """
    return all(dictionary.values())


def check_cls_dictionary(cls_dict):
    """ validate cls dictionary (cls.__dict__) for Model

    :param cls_dict: dict for checking
    """
    if not compare_lists(cls_dict.get('all_fields', tuple()), cls_dict.get('fields_types', dict()).keys()):
        all_fields = tuple(cls_dict.get('all_fields', tuple()))
        if len(set(all_fields)) != len(all_fields):
            duplicate_field_names = set([name for name in all_fields if all_fields.count(name) > 1])
            raise ValueError("Duplicate fields: {duplicate_fields}".format(
                duplicate_fields=duplicate_field_names))

    # check for empty types
    assert check_for_empty_values(cls_dict.get('fields_types', dict()))
    assert check_types_list(cls_dict.get('fields_types', dict()).values())

    # all fields must be defined in all_fields
    assert contain_all_elements(cls_dict.get('all_fields', tuple()), cls_dict.get('optional_fields', tuple()))
    assert contain_all_elements(cls_dict.get('all_fields', tuple()), cls_dict.get('default_values', dict()).keys())


def prepare_new_class(cls_dict, name):
    """ preparing a new class

    :param cls_dict: class for preparing
    :param name: class name
    """
    check_cls_dictionary(cls_dict)

    cls_dict['_all_fields'] = cls_dict.get('all_fields', tuple())
    cls_dict['_optional_fields'] = cls_dict.get('optional_fields', tuple())
    cls_dict['_default_values'] = cls_dict.get('default_values', dict())
    cls_dict['_fields_types'] = cls_dict.get('fields_types', dict())

    cls_dict.pop('all_fields', None)
    cls_dict.pop('optional_fields', None)
    cls_dict.pop('default_values', None)
    cls_dict.pop('fields_types', None)


def new_slots_class(mcs, name, bases, cls_dict):
    """ create new __slots__-based class

    :param mcs: metaclass
    :param name: name of new class
    :param bases: base classes
    :param cls_dict: __dict__ of new class
    :return: new object
    """
    prepare_new_class(cls_dict, name)

    cls_dict['__slots__'] = cls_dict.get('_all_fields', tuple())

    # conflicts __slots__ with class vars
    for item in cls_dict['__slots__']:
        cls_dict.pop(item, None)

    return type.__new__(mcs, name, bases, cls_dict)


def new_dict_class(mcs, name, bases, cls_dict):
    """ create new class

    :param mcs: metaclass
    :param name: name of new class
    :param bases: base classes
    :param cls_dict: __dict__ of new class
    :return: new object
    """
    prepare_new_class(cls_dict, name)

    return type.__new__(mcs, name, bases, cls_dict)


class Undefined(object):
    """ Class for detect undefined values"""


class BaseObjectModel(object):
    """ Base class for all models """
    __slots__ = tuple()
    _all_fields = tuple()
    _fields_types = dict()
    _default_values = dict()
    _optional_fields = dict()

    def init_model(self, kwargs):
        """ initialization all fields

        :param kwargs: data for initialization
        """
        for item in self._all_fields:
            if item not in kwargs and item not in self._default_values:
                if item not in self._optional_fields:
                    raise ValueError('required field {}'.format(item))
                else:
                    continue

            if item in kwargs:
                value = kwargs[item]
            else:
                value = self._default_values[item]

            self._set_attr(item, value)

    def _set_attr(self, key, value):
        """ set value (aka __setattr__)

        :param key: attr name
        :param value: attr value
        :return: None
        """
        # if value is None
        if type(value) in self._fields_types[key] or (value is None and value in self._fields_types[key]):
            setattr(self, key, value)
            return

        var_types = self._fields_types[key]

        if is_empty_string(value):

            if contain_str_type(var_types):
                setattr(self, key, "")
                return
            if contain_none(var_types):
                setattr(self, key, None)
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
            '`{}` must be type {}, got {} (`{}`) \n last err: {}\n types: {}'.format(key, types, type(value).__name__,
                                                                                     value,
                                                                                     err, var_types)
        )


class ObjectModelSlotsMetaclass(type):
    """ Metaclass for validate user definition a slots-based models """

    def __new__(mcs, name, bases, cls_dict):
        return new_slots_class(mcs, name, bases, cls_dict)


class ObjectModelDictMetaclass(type):
    """ Metaclass for validate user definition a models """

    def __new__(mcs, name, bases, cls_dict):
        return new_dict_class(mcs, name, bases, cls_dict)


class Field(object):
    """ Class for store definition field """

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
    """ Metaclass for validate user definition a pretty slots-based models """

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
    """ Metaclass for validate user definition a pretty models """

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


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""

    # Copyright (c) 2010-2017 Benjamin Peterson
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in all
    # copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.

    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class Metaclass(type):
        def __new__(mcs, name, this_bases, d):
            return meta(name, bases, d)

        @classmethod
        def __prepare__(mcs, name, this_bases):
            return meta.__prepare__(name, bases)

    return type.__new__(Metaclass, 'temporary_class', (), {})


if PY3:
    is_empty_string = _is_empty_string_py3
else:
    is_empty_string = _is_empty_string_py2
