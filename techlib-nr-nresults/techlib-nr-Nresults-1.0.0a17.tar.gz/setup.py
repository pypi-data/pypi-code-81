# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_nresults',
 'nr_nresults.jsonschemas',
 'nr_nresults.jsonschemas.nr_nresults',
 'nr_nresults.mapping_includes',
 'nr_nresults.mapping_includes.v7',
 'nr_nresults.mappings',
 'nr_nresults.mappings.v7',
 'nr_nresults.mappings.v7.nr_nresults',
 'nr_nresults.marshmallow']

package_data = \
{'': ['*']}

install_requires = \
['techlib-nr-common>=3.0.0a45,<4.0.0']

entry_points = \
{'invenio_base.api_apps': ['nr_nresults = nr_nresults:NRNresults'],
 'invenio_base.apps': ['nr_nresults = nr_nresults:NRNresults'],
 'invenio_jsonschemas.schemas': ['nr_nresults = nr_nresults.jsonschemas'],
 'invenio_pidstore.fetchers': ['nr_nresults = '
                               'nr_nresults.fetchers:nr_nresults_id_fetcher'],
 'invenio_pidstore.minters': ['nr_nresults = '
                              'nr_nresults.minters:nr_nresults_id_minter'],
 'invenio_search.mappings': ['nr_nresults = nr_nresults.mappings'],
 'oarepo_mapping_includes': ['nr_nresults = nr_nresults.mapping_includes']}

setup_kwargs = {
    'name': 'techlib-nr-nresults',
    'version': '1.0.0a17',
    'description': 'National repository Nresults metadata model',
    'long_description': '# nr-Nresults',
    'author': 'Daniel Kopecký',
    'author_email': 'Daniel.Kopecky@techlib.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
