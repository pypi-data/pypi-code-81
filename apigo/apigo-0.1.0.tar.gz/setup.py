# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apigo']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version >= "3.8" and python_version < "4.0"': ['importlib-metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['apigo = apigo.__main__:app']}

setup_kwargs = {
    'name': 'apigo',
    'version': '0.1.0',
    'description': 'get a fast REST mock server out of the box',
    'long_description': '# apigo\n\n<div align="center">\n\n[![Build status](https://github.com/nidhaloff/apigo/workflows/build/badge.svg?branch=master&event=push)](https://github.com/nidhaloff/apigo/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/apigo.svg)](https://pypi.org/project/apigo/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/nidhaloff/apigo/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/nidhaloff/apigo/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/nidhaloff/apigo/releases)\n[![License](https://img.shields.io/github/license/nidhaloff/apigo)](https://github.com/nidhaloff/apigo/blob/master/LICENSE)\n\nget a fast REST mock server out of the box\n\n</div>\n\n## Installation\n\n```bash\npip install -U apigo\n```\n\nor install with `Poetry`\n\n```bash\npoetry add apigo\n```\n\nThen you can run\n\n```bash\napigo --help\n```\n\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/nidhaloff/apigo)](https://github.com/nidhaloff/apigo/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/nidhaloff/apigo/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{apigo,\n  author = {nidhaloff},\n  title = {get a fast REST mock server out of the box},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/nidhaloff/apigo}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'nidhaloff',
    'author_email': 'nidhaloff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nidhaloff/apigo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
