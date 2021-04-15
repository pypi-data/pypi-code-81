#!/usr/bin/env python

"""The setup script."""
import time
from setuptools import setup, find_packages

version = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().split('\n')

setup(
    author="yuanjie",
    author_email='yuanjie@xiaomi.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    license="MIT license",
    description="CTR ZOO for CloudML",
    long_description=readme + '\n\n' + history,

    name='ctrzoo',
    keywords='ctrzoo',
    include_package_data=True,
    package_data={'': ['*.*']},
    packages=find_packages(),
    install_requires=requirements,

    test_suite='tests',
    url='https://github.com/Jie-Yuan/ctrzoo',
    version=version,  # '0.1.0',

    entry_points={
        'console_scripts': [
            'ctrzoo=ctrzoo.cli:main',
        ],
    },
)
