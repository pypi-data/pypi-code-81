# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfritz']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfritz',
    'version': '0.1.0',
    'description': 'Next gen fritzbox tool!',
    'long_description': '# pyfritz\n\n[![Build Status](https://github.com/cruisen/pyfritz/workflows/test/badge.svg?branch=master&event=push)](https://github.com/cruisen/pyfritz/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/cruisen/pyfritz/branch/master/graph/badge.svg)](https://codecov.io/gh/cruisen/pyfritz)\n[![Python Version](https://img.shields.io/pypi/pyversions/pyfritz.svg)](https://pypi.org/project/pyfritz/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nNext gen fritzbox tool!\n\n- Inspired by [fritzconnection](https://pypi.org/project/fritzconnection/)\n- Please note: not even Beta yet. Please stand by\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n\n## Installation\n\n```bash\npip install pyfritz\n```\n\n\n## Example\n\n```python\nimport pyfritz\n\n```\n\n## License\n\n[MIT](https://github.com/cruisen/pyfritz/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [fa093f1d48d9d41ecd53e18f19889393d1f11001](https://github.com/wemake-services/wemake-python-package/tree/fa093f1d48d9d41ecd53e18f19889393d1f11001). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/fa093f1d48d9d41ecd53e18f19889393d1f11001...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cruisen/pyfritz',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
