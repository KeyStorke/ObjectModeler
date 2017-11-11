import unittest

from object_modeler import Field
from object_modeler import GenericDictObjectModel, PrettyDictObjectModel
from object_modeler import GenericSlotsObjectModel,PrettySlotsObjectModel

test_dict = {
    'a': '1',
    'b': 'q',
    'c': None,
    'd': "",
    'O': 'test'
}

correct_dict = {
    'a': '1',
    'b': 'q',
    'c': 'None',
    'd': None
}


class A(GenericSlotsObjectModel):
    all_fields = ('a', 'b', 'c', 'd')
    optional_fields = ('b',)
    default_values = {'a': None}
    fields_types = {
        'a': (str,),
        'b': (str,),
        'c': (str,),
        'd': (None,)
    }

    def __init__(self, data):
        self.init_model(data)


class B(GenericDictObjectModel):
    all_fields = ('a', 'b', 'c', 'd')
    optional_fields = ('b',)
    default_values = {'a': None}
    fields_types = {
        'a': (str,),
        'b': (str,),
        'c': (str,),
        'd': (None,)
    }

    def __init__(self, data):
        self.init_model(data)


class C(PrettyDictObjectModel):
    a = Field(types=(str,), default_value=None)
    b = Field(types=(str,), optional=True)
    c = Field(types=(str,))
    d = Field(types=(None,))


class SomeClass:
    @staticmethod
    def test():
        return "all correct"


class C2(PrettyDictObjectModel):
    X = "all correct"


class D(C, C2, SomeClass): pass


class E(PrettySlotsObjectModel):
    __slots__ = tuple()
    a = Field(types=(str,), default_value=None)
    b = Field(types=(str,), optional=True)
    c = Field(types=(str,))
    d = Field(types=(None,))


class E2(E):
    e = Field(types=(int,), default_value=10)

    def test(self):
        return 21

    @staticmethod
    def static_test():
        return 31


class TestGenericSlotsObjectModel(unittest.TestCase):
    def setUp(self):
        self.a = A(test_dict)

    def test_constructor(self):
        self.assertTrue(self.a.a == '1')
        self.assertTrue(self.a.b == 'q')
        self.assertTrue(self.a.c == 'None')
        self.assertTrue(self.a.d is None)

    def test_mutable(self):
        with self.assertRaises(AttributeError):
            self.a.x = 1

    def test_overhead_data_in_constructor(self):
        with self.assertRaises(AttributeError):
            return self.a.O

    def test_to_dict(self):
        self.assertDictEqual(correct_dict, self.a.to_dict())

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'A')


class TestGenericDictObjectModel(unittest.TestCase):
    def setUp(self):
        self.a = B(test_dict)

    def test_constructor(self):
        self.assertEqual(self.a.a, '1')
        self.assertEqual(self.a.b, 'q')
        self.assertEqual(self.a.c, 'None')
        self.assertEqual(self.a.d, None)

    def test_mutable(self):
        self.a.x = 1
        self.assertEqual(self.a.x, 1)

    def test_overhead_data_in_constructor(self):
        with self.assertRaises(AttributeError):
            return self.a.O

    def test_to_dict(self):
        self.assertDictEqual(correct_dict, self.a.to_dict())

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'B')


class TestPrettyDictObjectModel(unittest.TestCase):
    def setUp(self):
        self.a = C(test_dict)

    def test_constructor(self):
        self.assertEqual(self.a.a, '1')
        self.assertEqual(self.a.b, 'q')
        self.assertEqual(self.a.c, 'None')
        self.assertEqual(self.a.d, None)

    def test_mutable(self):
        self.a.x = 1
        self.assertEqual(self.a.x, 1)

    def test_overhead_data_in_constructor(self):
        with self.assertRaises(AttributeError):
            return self.a.O

    def test_to_dict(self):
        self.assertDictEqual(correct_dict, self.a.to_dict())

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'C')


class TestPrettySlotsObjectModel(unittest.TestCase):
    def setUp(self):
        self.a = E(test_dict)

    def test_constructor(self):
        self.assertEqual(self.a.a, '1')
        self.assertEqual(self.a.b, 'q')
        self.assertEqual(self.a.c, 'None')
        self.assertEqual(self.a.d, None)

    def test_mutable(self):
        with self.assertRaises(AttributeError):
            self.a.x = 1

    def test_overhead_data_in_constructor(self):
        with self.assertRaises(AttributeError):
            return self.a.O

    def test_to_dict(self):
        self.assertDictEqual(correct_dict, self.a.to_dict())

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'E')


class TestInheritancePrettySlotsObjectModel(unittest.TestCase):
    def setUp(self):
        self.a = E2(test_dict)

    def test_constructor(self):
        self.assertEqual(self.a.a, '1')
        self.assertEqual(self.a.b, 'q')
        self.assertEqual(self.a.c, 'None')
        self.assertEqual(self.a.d, None)

    def test_mutable(self):
        with self.assertRaises(AttributeError):
            self.a.x = 1

    def test_overhead_data_in_constructor(self):
        with self.assertRaises(AttributeError):
            return self.a.O

    def test_to_dict(self):
        _test_dict = self.a.to_dict()
        _test_dict.pop('e', None)
        self.assertDictEqual(correct_dict, _test_dict)

    def test_inheritance_var(self):
        self.assertEqual(self.a.e, 10)

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'E2')

    def test_inherited_method(self):
        self.assertEqual(self.a.test(), 21)
        self.assertEqual(self.a.static_test(), 31)


class TestInheritancePrettyDictObjectModel(unittest.TestCase):
    def setUp(self):
        self.a = D(test_dict)

    def test_constructor(self):
        self.assertEqual(self.a.a, '1')
        self.assertEqual(self.a.b, 'q')
        self.assertEqual(self.a.c, 'None')
        self.assertEqual(self.a.d, None)

    def test_mutable(self):
        self.a.x = 1
        self.assertEqual(self.a.x, 1)

    def test_overhead_data_in_constructor(self):
        with self.assertRaises(AttributeError):
            return self.a.O

    def test_to_dict(self):
        self.assertDictEqual(correct_dict, self.a.to_dict())

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'D')

    def test_inherited_method(self):
        self.assertEqual(self.a.test(), "all correct")

    def test_inherited_attribute(self):
        self.assertEqual(self.a.X, "all correct")
