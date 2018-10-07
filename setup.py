from setuptools import setup

setup(
    test_suite='test',
    name='object_modeler',
    version='1.0.1',
    packages=['object_modeler'],
    install_requires=[
        'pyyaml'
    ],
    url='https://github.com/KeyStorke/ObjectModeler',
    license='MIT',
    author='Nickolay Ovdienko',
    author_email='Nickolay.Ovdienko@emc.com',
    description='Clearly and simply define objects schemes'
)
