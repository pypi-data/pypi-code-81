from setuptools import find_packages,setup

import graphmanagerlib

setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='0.6.0',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow', 'pandas', 'networkx', 'torch==1.8.0', 'torch-geometric', 'stellargraph'],
)