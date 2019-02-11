import yaml
from .slots_object_model import SlotsObjectModel
from .common import Undefined, Field
import importlib
import sys

PY3 = sys.version_info >= (3, 0)

if PY3:
    unicode = str

# types from the open api specification (see details: https://swagger.io/docs/specification/data-models/data-types/)

TYPES = {
    'string': unicode,
    'number': float,
    'integer': int,
    'boolean': bool,
    'array': list,
    'object': dict,
    'null': None,
}


def load_model(yaml_file):
    serializers = dict()
    values = dict()

    with open(yaml_file, 'r') as opened_file:
        data = dict(yaml.safe_load(opened_file))

    all_fields_names = tuple(field_name for field_name in data['fields'])
    optional_fields_names = tuple(field_name for field_name, value in data['fields'].items() if 'optional' in value)
    field_types_as_strings = {field_name: data['definition'][field_name]['type'] for field_name in all_fields_names if
                              data['definition'][field_name]['type'] is not None}
    field_types_as_strings.update(
        {field_name: 'null' for field_name in all_fields_names if data['definition'][field_name]['type'] is None})
    field_types = dict()

    # load defined classes, getting default values and import serializers

    if 'types_definitions' in data:
        for type_name in data['types_definitions']:
            module = importlib.import_module(data['types_definitions'][type_name])
            TYPES[type_name] = getattr(module, type_name)

    if 'serializers_definitions' in data:
        for serializer_name in data['serializers_definitions']:
            module = importlib.import_module(data['serializers_definitions'][serializer_name])
            serializers[serializer_name] = getattr(module, serializer_name)

    if 'values_definitions' in data:
        for value_name in data['values_definitions']:
            module = importlib.import_module(data['values_definitions'][value_name])
            values[value_name] = getattr(module, value_name)

    default_values = dict()
    hidden_fields = dict()
    serializers = dict()

    for field_name in all_fields_names:
        hidden_fields[field_name] = data['definition'][field_name].get('hidden', False)
        default_value = data['definition'][field_name].get('default_value', Undefined())

        if default_value in values:
            default_values[field_name] = values[default_value]
        else:
            default_values[field_name] = default_value

        serializer_name = data['definition'][field_name].get('serializer', None)
        serializers[field_name] = serializers.get(serializer_name, Undefined)

        if isinstance(field_types_as_strings[field_name], list):
            types = tuple([TYPES[typename] for typename in field_types_as_strings[field_name]])
        else:
            types = tuple([TYPES[field_types_as_strings[field_name]]])

        field_types[field_name] = types

    # yaml parsed

    # generate metadata for creation new class

    _class_data = {
        '_all_fields': all_fields_names,
        '_fields_types': field_types,
        '_default_values': default_values,
        '_optional_fields': optional_fields_names,
        '_hidden_fields': hidden_fields,
        '_serializers': serializers,
    }

    class_data = {}

    # generate new data model by generated metadata

    for field_name in _class_data['_all_fields']:
        field_is_optional = field_name in _class_data['_optional_fields']
        field_is_hidden = _class_data['_hidden_fields'][field_name]
        field_default_val = _class_data['_default_values'].get(field_name, Undefined())
        field_serializer = _class_data['_serializers'].get(field_name, Undefined())
        field_types = _class_data['_fields_types'][field_name]

        field = Field(
            types=field_types,
            optional=field_is_optional,
            default_value=field_default_val,
            hidden=field_is_hidden,
            serializer=field_serializer
        )

        class_data[field_name] = field

    return type(data['model_name'], (SlotsObjectModel,), class_data)
