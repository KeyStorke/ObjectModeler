from time import time

from object_modeler import PrettySlotsObjectModel, PrettyDictObjectModel, Field


class SomeClass(PrettySlotsObjectModel):
    a = Field(types=(str,))


class SomeClass2:
    def __init__(self, some_dict):
        self.__dict__.update(some_dict)


class SomeClass3(PrettyDictObjectModel):
    a = Field(types=(str,))


class SomeClass4:
    __slots__ = ('a',)

    def __init__(self, some_dict):
        for i in some_dict:
            setattr(self, i, some_dict[i])


some_dict = {'a': '1'}
N = 10 ** 6
all_time = 0

for _ in range(N):
    t1 = time()
    obj = SomeClass(some_dict)
    t2 = time()
    assert obj.a == '1'
    all_time += (t2 - t1)
print('PrettySlotsObjectModel results:')
print('     Average create object {} micro sec'.format((all_time / N) / 10 ** -6))
print('     Sum {} sec'.format(all_time))
print('')

all_time = 0

for _ in range(N):
    t1 = time()
    obj = SomeClass3(some_dict)
    t2 = time()
    assert obj.a == '1'
    all_time += (t2 - t1)
print('PrettyDictObjectModel results:')
print('     Average create object {} micro sec'.format((all_time / N) / 10 ** -6))
print('     Sum {} sec'.format(all_time))
print('')

all_time = 0

for _ in range(N):
    t1 = time()
    obj = SomeClass2(some_dict)
    t2 = time()
    assert obj.a == '1'
    all_time += (t2 - t1)

print('Standard dict class results:')
print('     Average create object {} micro sec'.format((all_time / N) / 10 ** -6))
print('     Sum {} sec'.format(all_time))
print('')

all_time = 0

for _ in range(N):
    t1 = time()
    obj = SomeClass4(some_dict)
    t2 = time()
    assert obj.a == '1'
    all_time += (t2 - t1)

print('Slots class results:')
print('     Average create object {} micro sec'.format((all_time / N) / 10 ** -6))
print('     Sum {} sec'.format(all_time))
print('')
