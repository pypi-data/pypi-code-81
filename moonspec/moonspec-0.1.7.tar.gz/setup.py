#!/usr/bin/env python

from setuptools import setup, find_packages

from moonspec import MOONSPEC_VERSION

with open('README.md') as f:
    readme = f.read()

setup(
    name='moonspec',
    version=MOONSPEC_VERSION,
    description='Infrastructure test framework',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Matiss Treinis',
    author_email='matiss@hub256.com',
    url='https://github.com/moonspec/moonspec',
    download_url='https://github.com/moonspec/moonspec',
    license='Apache 2.0',
    platforms='UNIX',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.20.0',
        'cryptography>=3.2',
    ],
    extras_require={
        'systemd_logging': ['systemd>=0.16.1'],
        'osquery_support': ['osquery>=3.0.6'],
        'libvirt_support': ['libvirt-python>=6.7.0'],
    },
    entry_points={
        'console_scripts': [
            'moonspec = moonspec.main:main',
        ]
    },
    data_files=[
        ('man/man1', ['docs/build/man/moonspec.1'])
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration',
    ],
)
