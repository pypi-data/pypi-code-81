# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_all']

package_data = \
{'': ['*'],
 'nr_all': ['translations/cs/LC_MESSAGES/*', 'translations/en/LC_MESSAGES/*']}

install_requires = \
['techlib-nr-Nresults>=1.0.0a13,<2.0.0',
 'techlib-nr-common>=3.0.0a45,<4.0.0',
 'techlib-nr-events>=1.0.0a14,<2.0.0',
 'techlib-nr-generic>=1.0.0a2,<2.0.0',
 'techlib-nr-theses>=1.0.0a3,<2.0.0']

entry_points = \
{'invenio_base.api_apps': ['nr_all = nr_all.ext:NRAll'],
 'invenio_base.apps': ['nr_all = nr_all.ext:NRAll'],
 'invenio_config.module': ['nr_all = nr_all.config'],
 'invenio_i18n.translations': ['nr_all = nr_all'],
 'invenio_pidstore.fetchers': ['nr_all = nr_all.fetchers:nr_all_id_fetcher'],
 'invenio_pidstore.minters': ['nr_all = nr_all.minters:nr_all_id_minter']}

setup_kwargs = {
    'name': 'techlib-nr-all',
    'version': '1.0.0a9',
    'description': 'Czech National Repository index that store all records from all metadata models',
    'long_description': '# nr-all\nCzech National Repository index that store all records from all metadata models.\n',
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
