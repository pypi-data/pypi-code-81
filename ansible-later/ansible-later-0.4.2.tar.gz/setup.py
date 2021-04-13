# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansiblelater',
 'ansiblelater.rules',
 'ansiblelater.test',
 'ansiblelater.test.unit',
 'ansiblelater.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'anyconfig>=0.10.0,<0.11.0',
 'appdirs>=1.4.4,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'flake8>=3.8.4,<4.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'nested-lookup>=0.2.21,<0.3.0',
 'pathspec>=0.8.1,<0.9.0',
 'python-json-logger>=2.0.1,<3.0.0',
 'six>=1.15.0,<2.0.0',
 'toolz>=0.11.1,<0.12.0',
 'unidiff>=0.6.0,<0.7.0',
 'yamllint>=1.25.0,<2.0.0']

extras_require = \
{'ansible': ['ansible>=3.0.0,<4.0.0'],
 'ansible-base': ['ansible-base>=2.10.4,<3.0.0']}

entry_points = \
{'console_scripts': ['ansible-later = ansiblelater.__main__:main']}

setup_kwargs = {
    'name': 'ansible-later',
    'version': '0.4.2',
    'description': 'Reviews ansible playbooks, roles and inventories and suggests improvements.',
    'long_description': '# ansible-later\n\nAnother best practice scanner for Ansible roles and playbooks\n\n[![Build Status](https://img.shields.io/drone/build/thegeeklab/ansible-later?logo=drone&server=https%3A%2F%2Fdrone.thegeeklab.de)](https://drone.thegeeklab.de/thegeeklab/ansible-later)\n[![Docker Hub](https://img.shields.io/badge/dockerhub-latest-blue.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/thegeeklab/ansible-later)\n[![Quay.io](https://img.shields.io/badge/quay-latest-blue.svg?logo=docker&logoColor=white)](https://quay.io/repository/thegeeklab/ansible-later)\n[![Python Version](https://img.shields.io/pypi/pyversions/ansible-later.svg)](https://pypi.org/project/ansible-later/)\n[![PyPI Status](https://img.shields.io/pypi/status/ansible-later.svg)](https://pypi.org/project/ansible-later/)\n[![PyPI Release](https://img.shields.io/pypi/v/ansible-later.svg)](https://pypi.org/project/ansible-later/)\n[![Codecov](https://img.shields.io/codecov/c/github/thegeeklab/ansible-later)](https://codecov.io/gh/thegeeklab/ansible-later)\n[![GitHub contributors](https://img.shields.io/github/contributors/thegeeklab/ansible-later)](https://github.com/thegeeklab/ansible-later/graphs/contributors)\n[![Source: GitHub](https://img.shields.io/badge/source-github-blue.svg?logo=github&logoColor=white)](https://github.com/thegeeklab/ansible-later)\n[![License: MIT](https://img.shields.io/github/license/thegeeklab/ansible-later)](https://github.com/thegeeklab/ansible-later/blob/main/LICENSE)\n\nansible-later is a best practice scanner and linting tool. In most cases, if you write Ansible roles in a team, it helps to have a coding or best practice guideline in place. This will make Ansible roles more readable for all maintainers and can reduce the troubleshooting time. While ansible-later aims to be a fast and easy to use linting tool for your Ansible resources, it might not be that feature completed as required in some situations. If you need a more in-depth analysis you can take a look at [ansible-lint](https://github.com/ansible-community/ansible-lint).\n\nansible-later does **not** ensure that your role will work as expected. For deployment tests you can use other tools like [molecule](https://github.com/ansible/molecule).\n\nYou can find the full documentation at [https://ansible-later.geekdocs.de](https://ansible-later.geekdocs.de/).\n\n## Community\n\n<!-- prettier-ignore-start -->\n<!-- spellchecker-disable -->\n\n- [GitHub Action](https://github.com/patrickjahns/ansible-later-action) by [@patrickjahns](https://github.com/patrickjahns)\n\n<!-- spellchecker-enable -->\n<!-- prettier-ignore-end -->\n\n## Contributors\n\nSpecial thanks goes to all [contributors](https://github.com/thegeeklab/ansible-later/graphs/contributors). If you would like to contribute,\nplease see the [instructions](https://github.com/thegeeklab/ansible-later/blob/main/CONTRIBUTING.md).\n\nansible-later is a fork of Will Thames [ansible-review](https://github.com/willthames/ansible-review). Thanks for your work on ansible-review and ansible-lint.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/thegeeklab/ansible-later/blob/main/LICENSE) file for details.\n',
    'author': 'Robert Kaussow',
    'author_email': 'mail@thegeeklab.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ansible-later.geekdocs.de/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
