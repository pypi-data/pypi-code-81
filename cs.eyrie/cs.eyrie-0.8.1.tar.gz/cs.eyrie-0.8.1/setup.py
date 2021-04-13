"""Setup for the cs.eyrie package."""

import setuptools
import os


# adapted from https://github.com/CrowdStrike/cs.eyrie/blob/master/setup.py
setuptools.setup(
    name='cs.eyrie',
    author="CrowdStrike, Inc.",
    author_email="csoc@crowdstrike.com",
    license="BSD",
    description='Eyrie - Retired',
    version='0.8.1',
    url='https://github.com/CrowdStrike/cs.eyrie',
    packages=setuptools.find_packages(),
    python_requires=">=2.7",
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 7 - Inactive',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: System :: Distributed Computing'
    ],
)
