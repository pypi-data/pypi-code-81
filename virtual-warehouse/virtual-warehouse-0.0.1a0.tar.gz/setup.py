# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virtual_warehouse', 'virtual_warehouse.parser']

package_data = \
{'': ['*'],
 'virtual_warehouse': ['resources/images/*',
                       'resources/images/textures/*',
                       'resources/objects/*',
                       'resources/qml/*']}

install_requires = \
['Owlready2==0.29',
 'PySide2==5.15.0',
 'openpyxl>=3.0.7,<4.0.0',
 'rdflib>=5.0.0,<6.0.0',
 'xlrd==1.2.0']

entry_points = \
{'console_scripts': ['virtual-warehouse = virtual_warehouse.__main__:main']}

setup_kwargs = {
    'name': 'virtual-warehouse',
    'version': '0.0.1a0',
    'description': 'Warehouse visualisation app',
    'long_description': '# Virtual Warehouse\n[![Documentation Status](https://readthedocs.org/projects/virtual-warehouse/badge/?version=latest)](https://virtual-warehouse.readthedocs.io/en/latest/?badge=latest) \n[![DeepSource](https://deepsource.io/gh/Breta01/virtual-warehouse.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/Breta01/virtual-warehouse/?ref=repository-badge)\n\nVisualisation of warehouse\n',
    'author': 'Břetislav Hájek',
    'author_email': 'info@bretahajek.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Breta01/virtual-warehouse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
