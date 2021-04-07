# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinybee']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.12.0,<0.13.0',
 'alive-progress>=1.6.2,<2.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'fetch-embed>=0.1.3,<0.2.0',
 'halo>=0.0.31,<0.0.32',
 'httpx>=0.17.1,<0.18.0',
 'joblib>=1.0.0,<2.0.0',
 'logzero>=1.6.3,<2.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'more-itertools>=8.6.0,<9.0.0',
 'morfessor>=2.0.6,<3.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'pycld2>=0.41,<0.42',
 'pyicu>=2.6,<3.0',
 'seaborn>=0.11.1,<0.12.0',
 'sentence-splitter>=1.4,<2.0',
 'statsmodels>=0.12.1,<0.13.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'tinybee',
    'version': '0.1.1',
    'description': 'A tiny aligner for dualtext alignment',
    'long_description': '# tinybee-aligner [![Codacy Badge](https://app.codacy.com/project/badge/Grade/0bef74fe4381412ab1172a06a93ad01e)](https://www.codacy.com/gh/ffreemt/tinybee-aligner/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/tinybee-aligner&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nA tiny alinger for dualtext alignment\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/tinybee-aligner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
