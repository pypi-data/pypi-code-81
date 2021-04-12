# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oc_graphenricher',
 'oc_graphenricher.APIs',
 'oc_graphenricher.enricher',
 'oc_graphenricher.instancematching']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'oc-graphenricher',
    'version': '0.1.0',
    'description': 'A tool to enrich any OCDM compliant Knowledge Graph, finding new identifiers and deduplicating entities',
    'long_description': None,
    'author': 'Gabriele Pisciotta',
    'author_email': 'ga.pisciotta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
