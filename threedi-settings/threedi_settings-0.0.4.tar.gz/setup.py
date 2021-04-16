#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = []

cmd_requirements = [
    "typer>=0.3.2",
    "rich>=10.1.0",
    "PyYAML>=5.1",
]

api_requirements = [
    'threedi-api-client>3.0.24'
]

test_requirements = ['pytest>=3', ]

setup(
    author="Lars Claussen",
    author_email='claussen.lars@nelen-schuurmans.nl',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Export legacy 3Di model settings to the 3Di API V3",
    install_requires=requirements,
    license="MIT license",
    long_description_content_type='text/markdown',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='threedi_settings',
    name='threedi_settings',
    packages=find_packages(include=['threedi_settings', 'threedi_settings.*']),
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        "console_scripts":  [
            "export-settings=threedi_settings.commands.export_legacy_settings:settings_app ",  # noqa
            "describe-simulation-settings=threedi_settings.commands.helpers:helper_app",  # noqa
            "global-settings=threedi_settings.commands.global_settings:global_settings_app",  # noqa
        ]
    },
    extras_require={
        'cmd': cmd_requirements,
        'api': api_requirements
    },
    url='https://github.com/nens/threedi-settings',
    version='0.0.4',
    zip_safe=False,
)
