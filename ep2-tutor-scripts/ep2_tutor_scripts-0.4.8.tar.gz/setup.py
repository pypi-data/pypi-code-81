#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name='ep2_tutor_scripts',
    version='0.4.8',
    author='Felix Resch',
    author_email='felix.resch@tuwien.ac.at',
    packages=['ep2_tutors', 'ep2_core'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ep2_ex_test=ep2_tutors.cli_ex_test:main',
            'ep2_eval=ep2_tutors.cli_eval:main',
            'ep2_util=ep2_tutors.cli_util:main',
        ]
    },
    install_requires=[
        'python-gitlab>=2.6.0',
        'click>=7.0',
        'gitpython>=3.1.0',
        'cheetah3>=3.2.0',
        'result>=0.5.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
