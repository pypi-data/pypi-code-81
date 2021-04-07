#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Boris Gailleton",
    author_email='boris.gailleton@gfz-potsdam.de',
    python_requires='>=3.5',
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
    description="Provides numba framework for topographic analysis within the LSDTopoTools ecosystem. It aims to provdide full python access to the main algorithms of LSDTopoTools while avoiding the neeeds of c++. It does not replace or provide numba portage of the full LSDTopoTools, just the main one for quick use or quick developments",
    entry_points={
        'console_scripts': [
            'lsdnumbatools=lsdnumbatools.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lsdnumbatools',
    name='lsdnumbatools',
    packages=find_packages(include=['lsdnumbatools', 'lsdnumbatools.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bgailleton/lsdnumbatools',
    version='0.0.1',
    zip_safe=False,
)
