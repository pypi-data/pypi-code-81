from setuptools import find_packages,setup


setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='0.9.6',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow',
                      'pandas',
                      'networkx',
                      'torch==1.8.0',
                      'torch-scatter==2.0.6',
                      'torch-geometric',
                      'stellargraph'],
)