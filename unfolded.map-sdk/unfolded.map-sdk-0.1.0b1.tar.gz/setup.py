#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
from glob import glob
from os.path import join as pjoin

from jupyter_packaging import (
    combine_commands, create_cmdclass, ensure_targets, get_version, install_npm)
from setuptools import find_namespace_packages, setup

HERE = os.path.dirname(os.path.abspath(__file__))

with open("README.md") as f:
    readme = f.read()

# The name of the project
name = 'unfolded.map-sdk'
# Directory as a tuple since we use namespace packaging
code_directory = ('unfolded', 'map_sdk')

# Get the version
version = get_version(pjoin(*code_directory, '_version.py'))

# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, *code_directory, 'nbextension', 'index.js'),
    pjoin(HERE, 'lib', 'plugin.js'), ]

package_data_spec = {name: ['nbextension/**js*', 'labextension/**']}

data_files_spec = [
    (
        'share/jupyter/nbextensions/unfolded/map_sdk',
        pjoin(*code_directory, 'nbextension'), '**'),

    # These are intended to be npm package name
    (
        'share/jupyter/labextensions/@unfolded/jupyter-map-sdk',
        pjoin(*code_directory, 'labextension'), '**'),
    (
        'share/jupyter/labextensions/@unfolded/jupyter-map-sdk', '.',
        'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.', 'unfolded.map_sdk.json')]

cmdclass = create_cmdclass(
    'jsdeps',
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:prod'),
    ensure_targets(jstargets),
)

setup_args = dict(
    name=name,
    description='Jupyter Widget for Unfolded.ai Maps',
    long_description=readme,
    long_description_content_type='text/markdown',
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    cmdclass=cmdclass,
    packages=find_namespace_packages(include=['unfolded.*']),
    author='UnfoldedInc.',
    author_email='info@unfolded.ai',
    license='Unlicensed',
    platforms='Linux, Mac OS X, Windows',
    keywords=['Jupyter', 'Widgets', 'IPython'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python', 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9', 'Framework :: Jupyter'],
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'deprecated', 'ipywidgets>=7.0.0', 'pydantic',
        'typing_extensions;python_version<"3.8"'],
    extras_require={
        'test': ['pytest>=4.6', 'pytest-cov', 'nbval', 'mypy'],
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'jupyter_sphinx', 'nbsphinx', 'nbsphinx-link', 'pytest_check_links',
            'pypandoc', 'recommonmark', 'sphinx>=1.5', 'sphinx_rtd_theme']},
    entry_points={},
)

if __name__ == '__main__':
    setup(**setup_args)
