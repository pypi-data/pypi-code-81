# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jhelper']

package_data = \
{'': ['*'],
 'jhelper': ['.mypy_cache/*',
             '.mypy_cache/3.8/*',
             '.mypy_cache/3.8/_typeshed/*',
             '.mypy_cache/3.8/collections/*',
             '.mypy_cache/3.8/email/*',
             '.mypy_cache/3.8/http/*',
             '.mypy_cache/3.8/importlib/*',
             '.mypy_cache/3.8/jhelper/*',
             '.mypy_cache/3.8/json/*',
             '.mypy_cache/3.8/logging/*',
             '.mypy_cache/3.8/os/*',
             '.mypy_cache/3.8/requests/*',
             '.mypy_cache/3.8/requests/packages/*',
             '.mypy_cache/3.8/requests/packages/urllib3/*',
             '.mypy_cache/3.8/requests/packages/urllib3/packages/*',
             '.mypy_cache/3.8/requests/packages/urllib3/packages/ssl_match_hostname/*',
             '.mypy_cache/3.8/requests/packages/urllib3/util/*',
             '.mypy_cache/3.8/urllib/*']}

install_requires = \
['filesplit>=3.0.2,<4.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['jhelper = jhelper.main:main']}

setup_kwargs = {
    'name': 'jhelper',
    'version': '0.1.1',
    'description': 'Juminfo Jenkins Upload Helper',
    'long_description': None,
    'author': 'ssfdust',
    'author_email': 'ssfdust@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
