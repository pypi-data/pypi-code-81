#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 15/04/21, 12:17 AM
#  License: See LICENSE.txt

import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Setup
setup(
    name='auto-clockify',
    version='0.0.4',
    description='Automation code snipplets to start and stop Clockify via API calls.',
    author='Adam Jakab',
    author_email='adam@jakab.pro',
    url='https://github.com/adamjakab/AutoClockify',
    license='MIT',
    long_description=README,
    long_description_content_type='text/markdown',
    platforms='ALL',

    include_package_data=True,
    test_suite='test',
    packages=['autoclockify'],
    entry_points={
        'console_scripts': [
            'auto_clockify = autoclockify.auto_clockify:main',
        ],
    },

    python_requires='>=3.6',

    install_requires=[
        'requests'
    ],

    tests_require=[
    ],

    # Extras needed during testing
    extras_require={
        'tests': [],
    },

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
    ],
)
