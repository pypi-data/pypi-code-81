# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irons',
 'irons.Functions.Data_management',
 'irons.Functions.Inflow_simulation',
 'irons.Functions.Reservoir_operating_policy',
 'irons.Functions.Reservoir_system_simulation',
 'irons.Functions.Weather_forecast',
 'irons.Functions.test_functions',
 'irons.Notebooks.A - Knowledge transfer.Inputs',
 'irons.Notebooks.A - Knowledge transfer.Modules']

package_data = \
{'': ['*'],
 'irons': ['Functions/.pytest_cache/*',
           'Functions/.pytest_cache/v/cache/*',
           'Functions/test_functions/.pytest_cache/*',
           'Functions/test_functions/.pytest_cache/v/cache/*']}

install_requires = \
['Functions>=0.7.0,<0.8.0',
 'bqplot==0.11.6',
 'cdsapi==0.2.5',
 'ipywidgets==7.2.1',
 'matplotlib==3.1.1',
 'netcdf4==1.4.2',
 'numba==0.49.1',
 'numpy==1.16.5',
 'pandas==0.25.1',
 'platypus-opt==1.0.3',
 'plotly==4.4.1']

setup_kwargs = {
    'name': 'irons',
    'version': '0.5',
    'description': 'A Python package that enables the simulation, forecasting and optimisation of reservoir systems',
    'long_description': None,
    'author': 'Andres Peñuela',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
