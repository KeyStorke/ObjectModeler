from setuptools import setup

setup(
    test_suite = 'test.py',
    name='object_modeler',
    version='0.0.9',
    packages=['object_modeler'],
    url='https://github.com/KeyStorke/ObjectModeler',
    license='MIT',
    author='Nickolay Ovdienko',
    author_email='Nickolay.Ovdienko@emc.com',
    description='Easy and simply define objects schemes in applications', requires=['six']
)
