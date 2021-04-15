from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'It\'s my first Python package bitch'

setup(
    name="quanmodule",
    version=VERSION,
    author="Quan Nham",
    author_email="beast@yeast.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['Quan', 'python', 'speedrun'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)