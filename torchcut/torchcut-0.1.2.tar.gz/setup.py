from setuptools import setup

setup(
    name='torchcut',
    version='0.1.2',
    author='Kristian Klemon',
    author_email='kristian.klemon@gmail.com',
    description='Shortcut for common PyTorch related imports.',
    packages=['torchcut'],
    install_requires=['torch'],
)
