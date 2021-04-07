# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grovec_sv_solution', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'click',
 'dask[complete]',
 'duckdb>=0.2.5,<0.3.0',
 'fastparquet>=0.5.0,<0.6.0',
 'ipykernel>=5.5.3,<6.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['grovec_sv_solution = grovec_sv_solution.cli:main']}

setup_kwargs = {
    'name': 'grovec-sv-solution',
    'version': '0.1.16',
    'description': 'Top-level package for GroveC-SV-Solution.',
    'long_description': '==================\nGroveC-SV-Solution\n==================\n\n\n.. image:: https://img.shields.io/pypi/v/grovec_sv_solution.svg\n        :target: https://pypi.python.org/pypi/grovec_sv_solution\n\n.. image:: https://img.shields.io/travis/sugix/grovec_sv_solution.svg\n        :target: https://travis-ci.com/sugix/grovec_sv_solution\n\n.. image:: https://readthedocs.org/projects/grovec-sv-solution/badge/?version=latest\n        :target: https://grovec-sv-solution.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/sugix/grovec_sv_solution/shield.svg\n     :target: https://pyup.io/repos/github/sugix/grovec_sv_solution/\n     :alt: Updates\n\n\n\nSolution for GroveCo TakeHome Test By SugiV\n\n\n* Free software: Apache-2.0\n* Documentation: https://grovec-sv-solution.readthedocs.io.\n\n\nFeatures\n--------\n\n* Airflow pipeline to daily ingest of neo data.\n* Airflow pipeline will be turned on automatically when you start Airflow\n',
    'author': 'Sugi Venugeethan',
    'author_email': 'sugi205@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sugix/grovec_sv_solution',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
