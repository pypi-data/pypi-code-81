# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hype_python_boilerplate']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.11.1,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['hype-python-boilerplate = '
                     'hype_python_boilerplate.console:main']}

setup_kwargs = {
    'name': 'hype-python-boilerplate',
    'version': '0.1.0',
    'description': 'hype-python-boilerplate, using example from cjolowicz.github.io',
    'long_description': '# hype-python-boilerplate\n\n[![Tests](https://github.com/ojefimow-test/hype-python-boilerplate/workflows/Tests/badge.svg)](https://github.com/ojefimow-test/hype-python-boilerplate/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/ojefimow-test/hype-python-boilerplate/branch/master/graph/badge.svg)](https://codecov.io/gh/ojefimow-test/hype-python-boilerplate)\n',
    'author': 'Alexei Efimov',
    'author_email': 'alexei.efimov@wirexapp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ojefimow-test/hype-python-boilerplate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
