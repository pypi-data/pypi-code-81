#!/usr/bin/env python
from setuptools import setup

setup(
    name='firefox_downloader',
    version='0.0.4',
    description='Download firefox and set desktop files',
    author='Riccardo Scartozzi',
    author_email='',
    url='https://gitlab.com/firefox2/firefox-utils.git',
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
