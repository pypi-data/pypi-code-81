# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['trio_serial']

package_data = \
{'': ['*']}

install_requires = \
['trio>=0.17,<1.0']

extras_require = \
{'docs': ['Sphinx>=3.4,<4.0',
          'sphinx-rtd-theme>=0.5,<1.0',
          'sphinxcontrib-trio>=1.1,<2.0']}

setup_kwargs = {
    'name': 'trio-serial',
    'version': '0.2.1',
    'description': 'Serial package for trio',
    'long_description': 'Serial package for trio\n=======================\nThis project is an adaption of the `pyserial <https://github.com/pyserial/pyserial/>`__ project\nfor `trio <https://github.com/python-trio/trio>`__.\n\nInstallation\n------------\n.. code-block:: console\n\n    $ pip install trio-serial\n\nDocumentation\n-------------\nhttps://trio-serial.1e8.de/\n',
    'author': 'Jörn Heissler',
    'author_email': 'nosuchaddress@joern-heissler.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joernheissler/trio-serial',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
