# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjwpandasmodule']

package_data = \
{'': ['*']}

install_requires = \
['cjwmodule>=4.0,<5.0', 'pandas>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'cjwpandasmodule',
    'version': '0.2.0',
    'description': 'Utilities for Workbench modules that use Pandas',
    'long_description': "Utilities for [CJWorkbench](https://github.com/CJWorkbench/cjworkbench) modules\nthat use Pandas.\n\nWorkbench modules may _optionally_ depend on the latest version of this Python\npackage for its handy utilities:\n\n* `cjwpandasmodule.validate`: functions to check if a DataFrame can be saved\n  in Workbench.\n\nDeveloping\n==========\n\n0. Run `tox` to confirm that unit tests pass\n1. Write a failing unit test in `tests/`\n2. Make it pass by editing code in `cjwpandasmodule/`\n3. Submit a pull request\n\nWe use [semver](https://semver.org/). Workbench will upgrade this dependency\n(minor version only) without module authors' explicit consent. Features in the\nsame major version must be backwards-compatible.\n\n\nPublishing\n==========\n\n1. ``git push`` and make sure Travis tests all pass.\n2. ``git tag vX.X.X``\n3. ``git push --tags``\n\nTravisCI will push to PyPi.\n",
    'author': 'Adam Hooper',
    'author_email': 'adam@adamhooper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
