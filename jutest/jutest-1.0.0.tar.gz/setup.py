import os
import re

import setuptools


def read_file(filename: str) -> str:
    current_directory = os.path.dirname(__file__)
    path = os.path.join(current_directory, filename)
    with open(path) as file:
        return file.read()


def get_version() -> str:
    code = read_file('jutest/__init__.py')
    return re.search(r'__version__ = \'(.*?)\'', code).group(1)


def get_long_description() -> str:
    return read_file('README.md')


setuptools.setup(
    name='jutest',
    version=get_version(),
    description='Library for easy testing CSV data using Jupyter notebook',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Alex Ermolaev',
    author_email='abionics.dev@gmail.com',
    keywords='test jupyter csv data testing',
    install_requires=[
        'IPython',
        'pandas',
        'Jinja2',
        'ahocorapy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=setuptools.find_packages(),
    zip_safe=False
)
