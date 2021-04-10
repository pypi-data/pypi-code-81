#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='gdata_subm',
    description=(
        'The submission library for sending data in the same format '
        'as collectd'
    ),
    version='0.1.5',
    author='Jay Deiman',
    author_email='admin@splitstreams.com',
    url='https://stuffivelearned.org',
    py_modules=['gdata_subm'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
    ],
)
