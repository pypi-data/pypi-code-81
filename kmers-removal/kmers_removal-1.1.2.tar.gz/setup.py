#!/usr/bin/env python3

__author__ = "DELEVOYE Guillaume"
__license__ = "MIT"
__version__ = "1.1.2"
__maintainer__ = "DELEVOYE Guillaume"
__email__ = "delevoye@ens.fr ; delevoye.guillaume@gmail.com"
__status__ = "Development"

from setuptools import setup, find_packages

setup(
    name='kmers_removal',
    description="Allows to remove user-specified lists of kmers from a genome assembly",
    version='1.1.2',
    author='DELEVOYE Guillaume',
    author_email="delevoye@ens.fr",
    packages=find_packages("."),
    url="https://github.com/GDelevoye/kmers_removal",
    package_data={'kmers_removal': ['notebook/*','testdata/*']},
    python_requires='>=3',
    install_requires=[
        'pandas',
        'tqdm',
        'argparse',
        'logging'
    ],
    entry_points={'console_scripts': [
        "kmers_removal = kmers_removal.kmers_removal_launcher:main"
    ]},
)
