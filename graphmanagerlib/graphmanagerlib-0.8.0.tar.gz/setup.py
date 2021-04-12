from setuptools import find_packages,setup

import graphmanagerlib

setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='0.8.0',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow', 'pandas', 'networkx', 'torch==1.8.0', 'torch-scatter', 'torch-sparse', 'torch-cluster', 'torch-spline-conv', 'torch-geometric', 'stellargraph'],
)