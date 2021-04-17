from setuptools import setup, find_packages
from distutils.cmd import Command
import os

# ['https://download.pytorch.org/whl/torch_stable.html']
install_requirements = [i.replace('\n','') for i in open('./requirements.txt').readlines()]

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'bert-embeddings',
    version = '0.0.9',
    description = 'Create positional embeddings based on TinyBERT or similar bert models',
    long_description = 'Bert Embeddings\n Use this library to really easily embed text using Bert Models.\n\n Github: https://github.com/sorcely/BertEmbeddings ' + '\n\n' + open('CHANGELOG.txt').read(),
    url = 'https://github.com/Sorcely/EmbeddingsLib',
    author = 'Marius J. Schlichtkrull',
    author_email = 'marius.schlichtkrull@gmail.com',
    license = 'MIT',
    classifiers = classifiers,
    keywords = 'embeddings',
    packages = find_packages(),
    install_requires = install_requirements,
)