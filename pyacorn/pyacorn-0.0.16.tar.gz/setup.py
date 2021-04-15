# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from glob import glob
from os import path

parent = path.abspath(path.dirname(__file__))
with open(path.join(parent, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyacorn',
    version='0.0.16',
    description="The python command-line client for the acorn platform",
    long_description=long_description,
    keywords='python acorn cli',
    project_urls={},
    packages=find_packages(exclude=['tests']),
    package_data={
        'pyacorn': [x[8:] for x in glob(
            'pyacorn/**/*.j2', recursive=True
        )],
    },
    install_requires=[
        'requests>=2.22.0,<3',
        'click>=7.1.1,<8',
        'jinja2>=2.10.3,<3',
        'pyfiglet',
        'commentjson',
    ],
    python_requires='>=3.5,<4',
    entry_points={
        'console_scripts': [
            'pyacorn = pyacorn.client:cli',
        ],
    }
)