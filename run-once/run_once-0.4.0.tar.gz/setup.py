# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['run_once']
install_requires = \
['grpcio>=1.15,<2.0', 'joblib>=1.0.1,<2.0.0', 'protobuf>=3.10,<4.0']

entry_points = \
{'console_scripts': ['distlock = run_once:_run_server']}

setup_kwargs = {
    'name': 'run-once',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Daeyun Shin',
    'author_email': 'daeyuns@uci.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
