#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import dreamtools

cfg = ["cfg/*.yml", '.env']

with open('README.md', encoding='utf-8') as readme:
    long_description = readme.read()


#setup------------------------------
setup(

    name='dreamtools-dreamgeeker',
    version=dreamtools.__version__,
    packages=find_packages(),
    author="dreamgeeker",
    author_email="dreamgeeker@couleurwest-it.com",
    description="outils de developpement de base",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['wheel', 'setuptools', 'pyaml', 'requests', 'cerberus', 'pillow', 'pytz',
                      "urllib3", "cerberus", "pillow", 'python-dotenv', 'verify_email', 'beautifulsoup4'],

    include_package_data=True,
    python_requires='>=3.8',
    url='https://github.com/couleurwest/dreamgeeker-tools',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development",
    ],
    package_data={'dreamtools': cfg},
    entry_points={
        'console_scripts': [
            'tools-installer = scripts.__main__:setproject'
        ]
    }
)
