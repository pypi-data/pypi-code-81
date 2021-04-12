# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# oarepo-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""OArepo module that adds support for communities"""

import os

from setuptools import find_packages, setup

readme = open('README.md').read()
history = open('CHANGES.md').read()

OAREPO_VERSION = os.environ.get('OAREPO_VERSION', '3.3.60')

tests_require = [
    'pydocstyle',
    'isort'
]

extras_require = {
    'tests': [
        'oarepo[tests]~={version}'.format(version=OAREPO_VERSION),
        *tests_require
    ]
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
]

install_requires = [
    'luqum'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('oarepo_search', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='oarepo-search',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio oarepo search',
    long_description_content_type='text/markdown',
    license='MIT',
    author='Daniel Kopecký',
    author_email='Daniel.Kopecky@techlib.cz',
    url='https://github.com/oarepo/oarepo-search',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        # 'flask.commands': [],
        'invenio_base.apps': [
            'oarepo_search = oarepo_search:OARepoSearch',
        ],
        'invenio_base.api_apps': [
            'oarepo_search = oarepo_search:OARepoSearch',
        ],
        # 'invenio_admin.actions': [],
        # 'invenio_access.system_roles': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        # 'invenio_db.models': [],
        # 'invenio_db.alembic': [],
        # 'invenio_base.api_converters': [],
        # 'invenio_base.converters': [],
        # 'oarepo_mapping_includes': [],
        # 'invenio_jsonschemas.schemas': [],
        # 'invenio_pidstore.minters': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 4 - Beta',
    ],
)
