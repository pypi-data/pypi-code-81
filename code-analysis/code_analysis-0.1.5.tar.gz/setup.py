#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Stefan Braun",
    author_email='sb@stbraun.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Analyze source code dependencies and call trees in Neo4j.",
    entry_points={
        'console_scripts': [
            'java_call_tree=code_analysis.java_call_tree:main',
            'java_dependencies=code_analysis.java_dependencies:main',
            'python_dependencies=code_analysis.python_dependencies:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='code_analysis',
    name='code_analysis',
    packages=find_packages(include=['code_analysis']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/stbraun/code_analysis',
    version='0.1.5',
    zip_safe=False,
)
