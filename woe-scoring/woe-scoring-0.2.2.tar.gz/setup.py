# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['woe_scoring', 'woe_scoring.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'woe-scoring',
    'version': '0.2.2',
    'description': 'Weight Of Evidence Transformer and LogisticRegression model with scikit-learn API',
    'long_description': None,
    'author': 'Kirill Stroganov',
    'author_email': 'kiraplenkin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
