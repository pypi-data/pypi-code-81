#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='fastbot',
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'write_to': 'fastbot/_version.py',
    },
    description='An sdk for building enterprise-grade conversational experiences',
    long_description=(
        open('README.md').read()
    ),
    long_description_content_type="text/markdown",
    author='Allen',
    author_email='allen@atlabs.dev',
    url='https://github.com/getfastbot/python',
    project_urls={
        "Documentation": "https://github.com/getfastbot/python",
        "Source": "https://github.com/getfastbot/python",
    },
    packages=find_packages(where="."),
    license='Proprietary License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    extras_require={
        'all': ['redis', 'pymemcache'],
        'redis': ['redis'],
        'memcached': ['pymemcache'],
    },
)
