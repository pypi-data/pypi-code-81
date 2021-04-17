from setuptools import setup

setup(
    name='msg2apps',
    version='v1.0',
    description='A module for sending messages to communication apps',
    py_modules=['msg2apps'],
    author='Daksimz',
    author_email='daksimzhang@gmail.com',
    url='https://github.com/daksim/msg2apps',
    requires=['requests', 'json'],
    license='MIT'
)