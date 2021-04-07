# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['amo_partner_crawler']

package_data = \
{'': ['*']}

install_requires = \
['datedelta>=1.3,<2.0', 'pydantic>=1.8.1,<2.0.0', 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'amo-partner-crawler',
    'version': '2.0.8',
    'description': 'SELENIUM CRAWLER FOR SCRAPING BILLING DATA FROM AMOCRM PARTNER CABINET',
    'long_description': None,
    'author': 'Igor Romaschenko',
    'author_email': 'rocinantt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
