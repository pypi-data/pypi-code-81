#!/usr/bin/env python3
from setuptools import setup


from djangocms_helpers import __version__


setup(
    name='djangocms-helpers',
    version=__version__,
    author='Victor',
    author_email='victor@what.digital',
    url='https://gitlab.com/what-digital/djangocms-helpers',
    packages=[
        'djangocms_helpers',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 2.2, < 4',
        'django-fieldsignals >= 0.4.0',
        'django-meta',
    ],
)
