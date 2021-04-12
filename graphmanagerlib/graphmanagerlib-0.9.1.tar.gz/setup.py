from setuptools import find_packages,setup

import graphmanagerlib

setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='0.9.1',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow',
                      'pandas',
                      'networkx',
                      'torch==1.8.0',
                      'torch-scatter @ https://pytorch-geometric.com/whl/torch-1.8.0+cpu.html',
                      'torch-sparse @ https://pytorch-geometric.com/whl/torch-1.8.0+cpu.html',
                      'torch-cluster @ https://pytorch-geometric.com/whl/torch-1.8.0+cpu.html',
                      'torch-spline-conv @ https://pytorch-geometric.com/whl/torch-1.8.0+cpu.html',
                      'stellargraph'],
)