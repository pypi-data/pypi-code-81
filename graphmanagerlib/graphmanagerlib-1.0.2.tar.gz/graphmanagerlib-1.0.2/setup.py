from setuptools import find_packages,setup


setup(
    name='graphmanagerlib',
    packages=find_packages(),
    version='1.0.2',
    description='My first Python library',
    author='Cambier Damien',
    license='MIT',
    install_requires=['tensorflow',
                      'pandas',
                      'networkx',
                      'torch==1.8.0',
                      'torch-geometric',
                      'bpemb',
                      'sentence_transformers',
                      'stellargraph'],
)