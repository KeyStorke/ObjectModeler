from time import time

from object_modeler import SlotsObjectModel, ObjectModel, Field
from string import ascii_lowercase


class SomeClass(SlotsObjectModel):
    a = Field().types(str)
    b = Field().types(int)
    c = Field().types(bool)


class SomeClass2(ObjectModel):
    a = Field().types(str)
    b = Field().types(int)
    c = Field().types(bool)


class SomeClass3:
    fields = ('a', 'b', 'c')

    def __init__(self, some_dict):
        for item in self.fields:
            if item in some_dict:
                setattr(self, item, some_dict[item])
            else:
                raise ValueError


class SomeClass4:
    __slots__ = ('a', 'b', 'c')

    def __init__(self, some_dict):
        for item in self.__slots__:
            if item in some_dict:
                setattr(self, item, some_dict[item])
            else:
                raise ValueError


def benchmark_it(cls, name):
    some_dict = {char: '1' for char in ascii_lowercase}
    big_dict = {key: key+1 for key in range(10**6)}
    some_dict.update(big_dict)

    N = 10 ** 6
    all_time = 0

    min_ = 10**6
    max_ = 0

    for _ in range(N):
        obj = cls(some_dict)
        assert obj.a == '1'

    for _ in range(N):
        t1 = time()
        obj = cls(some_dict)
        t2 = time()
        assert obj.a == '1'

        duration = t2 - t1

        if duration < min_:
            min_ = duration
        if duration > max_:
            max_ = duration

        all_time += duration

    print('{} results:'.format(name))
    print('     Average create object {} micro sec'.format((all_time / N) / 10 ** -6))
    print('     Sum {} sec'.format(all_time))
    print('     Min {} micro sec'.format(min_ / 10 ** -6))
    print('     Max {} micro sec'.format(max_ / 10 ** -6))
    print('')


benchmark_it(SomeClass4, 'Standard slots class')
benchmark_it(SomeClass3, 'Standard dict class')
benchmark_it(SomeClass, 'PrettySlotsObjectModel')
benchmark_it(SomeClass2, 'PrettyDictObjectModel')
