from setuptools import setup

with open('README.md') as fp:
    long_description = fp.read()

setup(
    name = 'Elite',
    version = '1.1.0',
    author = 'origamizyt',
    author_email = 'zhaoyitong18@163.com',
    description = 'A lightweight module for elliptic-curve security schemes.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3',
    install_requires = ['ecdsa', 'PyCryptodome'],
    url = 'https://github.com/origamizyt/Elite',
    packages = ['elite']
    )
