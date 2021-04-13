#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name='ep2_tech_scripts',
    version='0.4.3',
    author='Felix Resch',
    author_email='felix.resch@tuwien.ac.at',
    packages=['ep2_tech'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ep2_tech=ep2_tech.cli_tech:main'
        ]
    },
    install_requires=[
        'click>=7.0',
        'gitpython>=3.1.0',
        'result>=0.5.0',
        'ep2_tutor_scripts>=0.4.2',
        'terminaltables>=3.1.0',
        'PyYAML>=5.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
