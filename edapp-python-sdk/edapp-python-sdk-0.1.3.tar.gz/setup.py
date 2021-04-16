# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edapp_python_sdk']

package_data = \
{'': ['*']}

install_requires = \
['html2text>=2020.1.16,<2021.0.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'tqdm>=4.58.0,<5.0.0',
 'xlsxwriter>=1.3.7,<2.0.0']

entry_points = \
{'console_scripts': ['edapp_create_groups = '
                     'edapp_python_sdk.main:create_new_groups',
                     'edapp_export = edapp_python_sdk.main:edapp_export',
                     'edapp_survey_report = '
                     'edapp_python_sdk.main:export_survey_report']}

setup_kwargs = {
    'name': 'edapp-python-sdk',
    'version': '0.1.3',
    'description': 'A Python tool for interacting with the EdApp SDK',
    'long_description': None,
    'author': 'Edd Abrahamsen-Mills',
    'author_email': 'edward.abrahamsen-mills@safetyculture.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
