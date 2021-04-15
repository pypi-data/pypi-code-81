#!/usr/bin/env python
from setuptools import setup

setup(
    name='firefox_downloader',
    version='0.0.1',
    description='Download firefox and set desktop files',
    author='Riccardo Scartozzi',
    author_email='',
    url='https://github.com/claranet/python-terrafile',
    license='MIT License',
    packages=(
        'firefox_downloader',
    ),
    scripts=(
        'bin/firefox_downloader',
    ),
    install_requires=(
        'requests',
    ),
)
