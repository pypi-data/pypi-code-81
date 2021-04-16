# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambda_utility']

package_data = \
{'': ['*']}

install_requires = \
['aiobotocore>=1.3.0,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'slack-sdk>=3.4.2,<4.0.0']

setup_kwargs = {
    'name': 'lambda-utility',
    'version': '0.8.2',
    'description': '',
    'long_description': "# lambda-utility\n[![Python](https://img.shields.io/badge/python-v3.9-blue.svg?&logo=python&style=flat)](https://docs.python.org/3.9/)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\nAWS Lambda에서 자주 사용하는 기능 구현\n\n## Installation\nPython 3.7 +\n```bash\n$ pip install lambda-utility\n```\n\n## Create a layer file\n```bash\n$ python layer\n\n...\nComplete -> 'lambda-utility.zip'\n```\nor\n```bash\n$ python layer -o {filename}\n\n...\nComplete -> '{filename}'\n```\n",
    'author': 'Kyungmin Lee',
    'author_email': 'rekyungmin@gmail.com',
    'maintainer': 'Kyungmin Lee',
    'maintainer_email': 'rekyungmin@gmail.com',
    'url': 'https://github.com/rekyungmin/lambda-utility',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
