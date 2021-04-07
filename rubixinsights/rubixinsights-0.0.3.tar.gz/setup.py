# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rubixinsights']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3.1',
 'SQLAlchemy==1.3.23',
 'boto3==1.16.40',
 'pandas==1.2.2',
 'psycopg2-binary==2.8.6',
 'requests==2.25.1']

setup_kwargs = {
    'name': 'rubixinsights',
    'version': '0.0.3',
    'description': 'rubixin-sights',
    'long_description': '# insights-helper-functions\nHelper and Utility Functions\n',
    'author': 'rubix',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
