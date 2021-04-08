#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "pandas",
    "pysam"
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Tom Kuipers",
    author_email='t.b.kuipers@lumc.nl',
    python_requires='>3',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Prepare expression data for dgeAnalysis - LUMC.",
    entry_points={
        'console_scripts': [
            'predex=predex.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='predex',
    name='predex',
    packages=find_packages(include=['predex', 'predex.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tomkuipers1402/predex',
    version='0.9.3',
    zip_safe=False,
)
