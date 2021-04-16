#!/usr/bin/env python3
"""s2reader3 setup configuration."""

from setuptools import setup

setup(
    name='s2reader3',
    version='0.6.3',
    description='simple Python 3 metadata reader for Sentinel-2 SAFE files (Level-1C and Level-2A), derived from old unsupported Python 2 s2reader3 of https://github.com/ungarj/s2reader.git',
    author='Leonid Kolesnichenko',
    author_email='xperience439@gmail.com',
    url='https://github.com/robert-werner/s2reader3.git',
    license='MIT',
    packages=[  # TODO fix module structure
        's2reader3', 's2reader3.cli'
    ],
    entry_points={
        'console_scripts': [
            's2_inspect = s2reader3.cli.inspect:main',
            's2_transform = s2reader3.cli.transform:main'
        ],
    },
    install_requires=[
        'lxml',
        'shapely',
        'numpy',
        'pyproj',
        'cached_property',
        'zipfile2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
