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
    'version': '0.2.1',
    'description': 'A convenience library to read and alter PDFs to remove personally identifying data',
    'long_description': '# Pseudonymize PDF\nA convenience library to read and alter PDFs to remove personally identifying data.\n',
    'author': 'Stephen Badger',
    'author_email': 'stephen.badger@vitalbeats.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vitalbeats/pseudonymize-pdf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
