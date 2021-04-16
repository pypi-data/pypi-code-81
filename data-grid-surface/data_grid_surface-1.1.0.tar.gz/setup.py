# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'data_grid_surface'}

packages = \
['config',
 'data_grid_surface',
 'data_grid_surface.config',
 'data_grid_surface.services']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'data-grid-surface',
    'version': '1.1.0',
    'description': 'SDK to communicate with data-grid API',
    'long_description': "\n# DATA-GRID-SURFACE\nSDK to communicate with data-grid API service.\nIt uses the API service and it's end-points to determine if the given emails or passwords have been compromised.\n\n\n## Installation\n\nInstall data-grid-surface SDK:\n\n```\npip install data-grid-surface\n```\n\n## Using data-grid-access sdk\n\nImport DataGrid class from library\n\n```\nfrom data_grid_surface.data_grid import DataGrid\n```\n\nYou will need to provide username and password parameters to DataGrid class constructor. These are credentials for data-grid API service.\n\nNOTE: Passwords and emails are hashed with SHA256 algorithm before being sent to the API service.\n\n### DataGrid methods\n\nDataGrid methods return dictionary as a result.\n\nYou can pass raw email/password or its hashed value. If you are passing hashed value you need to hash it with SHA256 algorithm and encode it in base64 format.\n\n**Methods:**\n* check_email(email, is_hashed) \n    * email **_\\<String\\>_**\n    * is_hashed **_\\<Boolean\\>_** default value is True\n\n* check_password(password, is_hashed)\n    * password **_\\<String\\>_**\n    * is_hashed **_\\<Boolean\\>_** default value is True\n\n**Use example:**\n\n```\nfrom data_grid_surface.data_grid import DataGrid\n\ndg = DataGrid(\n    username='testuser', \n    password='testpassword'\n)\nres = dg.check_email('email@example.com', False)\n```\n\n```\nres = dg.check_password('passwordexample', False)\n```\n\n**Response:**\n\n```\n{\n    'status': 'success', \n    'data': {\n        'exposed': True|False\n    }\n}\n```",
    'author': 'DataGrid Dev Team',
    'author_email': 'dev@datagridsurface.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
