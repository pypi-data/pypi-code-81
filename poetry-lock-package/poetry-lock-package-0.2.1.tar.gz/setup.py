# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_lock_package']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'loguru>=0.5.3,<0.6.0', 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.22']}

entry_points = \
{'console_scripts': ['poetry-lock-package = poetry_lock_package.app:main']}

setup_kwargs = {
    'name': 'poetry-lock-package',
    'version': '0.2.1',
    'description': 'Poetry lock package generator',
    'long_description': "Poetry lock package generator\n=========================\n\n\nSimple script that will take a `pyproject.toml` and a `poetry.lock` and generate a new poetry project where all the lock versions are pinned dependencies.\n\nIn theory this will allow you to transport your lock file to any system that is able to install python packages and dependencies.\n\nAfter installation, the command `poetry-lock-package` should be run next to your `pyproject.toml` and `poetry.lock` files and will generate a subdirectory with a `pyproject.toml` requiring all the dependencies of the lock file.\n\nSimply enter the subdirectory, build and publish the package and you have a '-lock' package that depends on all the exact versions from your lock file.\n\n\nExample worflow\n---------------\n\nSimply put, the workflow is as follows\n\n    pip install poetry poetry-lock-package\n    poetry new example-package\n    cd example-package\n    poetry add loguru\n    poetry-lock-package\n    cd example-package-lock\n    cat pyproject.toml\n    poetry install\n\nContributing code\n-----------------\n\n- Open an issue\n- Create an associated PR\n- Make sure to black format the proposed change\n\n    poetry run pre-commit install\n\n- Add tests where possible\n\nLicense\n-------\nGPLv3, use at your own risk.\n\n",
    'author': 'Bram Neijt',
    'author_email': 'bram@neijt.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bneijt/poetry-lock-package',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
