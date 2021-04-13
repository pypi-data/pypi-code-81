from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="flexpepdock",
    version="1.0.9",
    author="nobel",
    author_email="nanjilincq@foxmail.com",
    description="A Python library for batch upload for flexpepdock.",
    long_description=open("README.rst").read(),
    license="MIT",
    #url="https://github.com/WEIHAITONG1/better-youtubedl",
    packages=['flexpepdock'],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Multimedia :: Video',
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'batchUpload = flexpepdock.main:main'
        ]
    },
    zip_safe=True,
    install_requires=[
	'requests_toolbelt', 'bs4', 'requests'
    ]
)
