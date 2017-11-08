import unittest
from slots_object_model import GenericSlotsObjectModel
from dict_object_model import GenericDictObjectModel

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
            a = self.a.O
            print(a)

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
            a = self.a.O
            print(a)

    def test_to_dict(self):
        self.assertDictEqual(correct_dict, self.a.to_dict())

    def test_name(self):
        self.assertEqual(self.a.__name__(), 'B')
