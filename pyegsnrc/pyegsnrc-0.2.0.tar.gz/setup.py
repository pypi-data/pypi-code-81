# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyegsnrc', 'pyegsnrc.data']

package_data = \
{'': ['*'], 'pyegsnrc.data': ['bremsstrahlung/*']}

install_requires = \
['jax', 'jaxlib', 'matplotlib', 'pandas', 'scipy', 'typer', 'typing-extensions']

entry_points = \
{'console_scripts': ['pyegsnrc = pyegsnrc.__main__:main']}

setup_kwargs = {
    'name': 'pyegsnrc',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
