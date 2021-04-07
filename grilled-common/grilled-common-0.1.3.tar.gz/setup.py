# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grilled', 'grilled.common', 'grilled.common.data_structure']

package_data = \
{'': ['*']}

install_requires = \
['logging>=0.4.9.6,<0.5.0.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'grilled-common',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'hans',
    'author_email': 'dxzenghan@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
