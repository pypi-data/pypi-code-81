# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pseudonymize_pdf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pseudonymize-pdf',
    'version': '0.2.0',
    'description': 'A convenience library to read and alter PDFs to remove personally identifying data',
    'long_description': None,
    'author': 'Stephen Badger',
    'author_email': 'stephen.badger@vitalbeats.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
