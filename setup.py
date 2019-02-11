from setuptools import setup

setup(
    test_suite='test',
    name='object_modeler',
    version='1.0.3',
    packages=['object_modeler'],
    install_requires=[
        'pyyaml'
    ],
    url='https://github.com/KeyStorke/ObjectModeler',
    license='MIT',
    author='Nickolay Ovdienko',
    author_email='Nickolay.Ovdienko@emc.com',
    description='Tool for clearly and simply definition of objects schemes'
)
