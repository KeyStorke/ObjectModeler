from time import time

from object_modeler import PrettySlotsObjectModel, PrettyDictObjectModel, Field


class SomeClass(PrettySlotsObjectModel):
    a = Field(types=(str,))


class SomeClass2(PrettyDictObjectModel):
    a = Field(types=(str,))


class SomeClass3:
    def __init__(self, some_dict):
        for i in some_dict:
            setattr(self, i, some_dict[i])


class SomeClass4:
    __slots__ = ('a',)

    def __init__(self, some_dict):
        for i in some_dict:
            if i in self.__slots__:
                setattr(self, i, some_dict[i])


def benchmark_it(cls, name):
    some_dict = {'a': '1'}
    N = 10 ** 6
    all_time = 0

    for _ in range(N):
        t1 = time()
        obj = cls(some_dict)
        t2 = time()
        assert obj.a == '1'
        all_time += (t2 - t1)
    print('{} results:'.format(name))
    print('     Average create object {} micro sec'.format((all_time / N) / 10 ** -6))
    print('     Sum {} sec'.format(all_time))
    print('')

benchmark_it(SomeClass, 'PrettySlotsObjectModel')
benchmark_it(SomeClass2, 'PrettyDictObjectModel')
benchmark_it(SomeClass3, 'Standard dict class')
benchmark_it(SomeClass4, 'Standard slots class')
