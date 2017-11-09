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


class ObjectModelSlotsMetaclass(type):
    def __new__(mcs, name, bases, cls_dict: dict):
        # for all fields must be defined data type
        assert compare_lists(cls_dict['all_fields'], cls_dict['fields_types'].keys())

        # all fields must be defined in all_fields
        assert contain_all_elements(cls_dict['all_fields'], cls_dict['optional_fields'])
        assert contain_all_elements(cls_dict['all_fields'], cls_dict['default_values'].keys())

        cls_dict['__slots__'] = cls_dict['all_fields']
        cls_dict['_optional_fields'] = cls_dict['optional_fields']
        cls_dict['_default_values'] = cls_dict['default_values']
        cls_dict['_fields_types'] = cls_dict['fields_types']

        cls_dict.pop('all_fields')
        cls_dict.pop('optional_fields')
        cls_dict.pop('default_values')
        cls_dict.pop('fields_types')

        return type.__new__(mcs, name, bases, cls_dict)


class ObjectModelDictMetaclass(type):
    def __new__(mcs, name, bases, cls_dict: dict):
        # for all fields must be defined data type
        assert compare_lists(cls_dict['all_fields'], cls_dict['fields_types'].keys())

        # all fields must be defined in all_fields
        assert contain_all_elements(cls_dict['all_fields'], cls_dict['optional_fields'])
        assert contain_all_elements(cls_dict['all_fields'], cls_dict['default_values'].keys())

        cls_dict['_all_fields'] = cls_dict['all_fields']
        cls_dict['_optional_fields'] = cls_dict['optional_fields']
        cls_dict['_default_values'] = cls_dict['default_values']
        cls_dict['_fields_types'] = cls_dict['fields_types']

        cls_dict.pop('all_fields')
        cls_dict.pop('optional_fields')
        cls_dict.pop('default_values')
        cls_dict.pop('fields_types')

        return type.__new__(mcs, name, bases, cls_dict)
