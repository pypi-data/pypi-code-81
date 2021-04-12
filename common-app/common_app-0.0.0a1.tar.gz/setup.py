# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['not_on_pypi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'common-app',
    'version': '0.0.0a1',
    'description': 'Reserved package name',
    'long_description': "# Not On PyPi\n\nThis is a reserved package name to prevent [dependency confusion / substitution attack](https://redhuntlabs.com/blog/dependency-confusion-attack-what-why-and-how.html). If installed, will immediately raise an error indicating that the wrong PyPi repository was used.\n\nIf someone would like to use this package name, I would be happy to discuss handoff. Please contact me through a Github issue on [KyleKing/not-on-pypi](https://github.com/KyleKing/not-on-pypi) or if I don't respond, you can try my `gmail` account `dev.act.kyle`\n",
    'author': 'Kyle King',
    'author_email': 'dev.act.kyle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KyleKing/not-on-pypi',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
