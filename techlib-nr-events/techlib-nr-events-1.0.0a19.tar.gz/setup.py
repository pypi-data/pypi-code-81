# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_events',
 'nr_events.jsonschemas',
 'nr_events.jsonschemas.nr_events',
 'nr_events.mapping_includes',
 'nr_events.mapping_includes.v7',
 'nr_events.mappings',
 'nr_events.mappings.v7',
 'nr_events.marshmallow']

package_data = \
{'': ['*'], 'nr_events.mappings.v7': ['nr_events/*']}

install_requires = \
['techlib-nr-common>=3.0.0a45,<4.0.0']

entry_points = \
{'invenio_base.api_apps': ['events = nr_events:NREvents'],
 'invenio_base.apps': ['events = nr_events:NREvents'],
 'invenio_jsonschemas.schemas': ['nr_events = nr_events.jsonschemas'],
 'invenio_pidstore.fetchers': ['nr_events = '
                               'nr_events.fetchers:nr_events_id_fetcher'],
 'invenio_pidstore.minters': ['nr_events = '
                              'nr_events.minters:nr_events_id_minter'],
 'invenio_search.mappings': ['nr_events = nr_events.mappings'],
 'oarepo_mapping_includes': ['nr_events = nr_events.mapping_includes']}

setup_kwargs = {
    'name': 'techlib-nr-events',
    'version': '1.0.0a19',
    'description': 'National repository events metadata model',
    'long_description': '# nr-events\nData model for events related records\n',
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
