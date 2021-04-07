# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ggci']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'pyyaml>=5.4.1,<6.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'ggci',
    'version': '0.1.2',
    'description': 'GitLab Google Chat Integration',
    'long_description': None,
    'author': 'Jan Lukány',
    'author_email': 'lukany.jan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
