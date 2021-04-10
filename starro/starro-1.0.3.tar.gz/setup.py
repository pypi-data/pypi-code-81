# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starro']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['coverage = scripts:coverage',
                     'lint = scripts:lint',
                     'security = scripts:security',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'starro',
    'version': '1.0.3',
    'description': 'The package objective is to mischaracterize sensitive data from this through blinding masks using asterisk',
    'long_description': None,
    'author': 'Marcos Borges',
    'author_email': 'contato@marcosborges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
