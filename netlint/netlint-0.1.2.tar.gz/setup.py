# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netlint',
 'netlint.checks',
 'netlint.checks.cisco_ios',
 'netlint.checks.cisco_nxos',
 'netlint.checks.various',
 'netlint.cli']

package_data = \
{'': ['*']}

install_requires = \
['ciscoconfparse>=1.5.30,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'toml>=0.10.2,<0.11.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{'docs': ['sphinx>=3.5.3,<4.0.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'm2r2>=0.2.7,<0.3.0']}

entry_points = \
{'console_scripts': ['netlint = netlint.cli.main:cli']}

setup_kwargs = {
    'name': 'netlint',
    'version': '0.1.2',
    'description': 'Performs static analysis on network device configuration files.',
    'long_description': '**Note: Still in active development and potentially subject to major changes - keep this in mind when using this.**\n\n# Netlint\n\n![Build workflog](https://github.com/Kircheneer/netlint/actions/workflows/main.yml/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/netlint/badge/?version=latest)](https://netlint.readthedocs.io/en/latest/?badge=latest)\n\nPerforms static analysis on network device configuration files.\n\nLinters have long since been a standard way of assessing code quality\nin the software development world. This project aims to take that idea\nand apply it to the world of network device configuration files.\n\nFind the latest copy of the documentation [here](https://netlint.readthedocs.io).\n\nPotential uses of this tool are\n\n- Linting network device configurations generated in\n  CI/CD automation pipelines\n- Assistance when building out new configurations for\n  both traditional and automated deployment\n- Basic security auditing of configuration files\n\n## Example usage\n\nBelow is an example of how to use this based on one of the faulty test\nconfigurations (executed from the project root):\n\n```\n$  netlint --nos cisco_ios tests/cisco_ios/configurations/faulty.conf\nIOS101 Plaintext user passwords in configuration.\n-> username test password ing\nIOS102 HTTP server not disabled\n-> ip http server\n-> ip http secure-server\nIOS103 Console line unauthenticated\n-> line con 0\n\n```\n\n## Installation\n\nThere are multiple ways of installing this software.\n\nA package is available on [PyPI](https://pypi.org/project/netlint/),\ntherefore you can simply install with `pip install netlint` and\nthen simply run `netlint`.\n\nIf you prefer to install directly from\nGitHub, here is how you would go about that.\n\n```bash\n$ git clone https://github.com/Kircheneer/netlint.git\n$ cd netlint\n$ pip install .\n$ netlint --help\nUsage: netlint [OPTIONS] COMMAND [ARGS]...\n\n  Lint network device configuration files.\n\n  [...]\n```\n',
    'author': 'Leo Kirchner',
    'author_email': 'leo@kirchne.red',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://netlint.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
