# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_spinproject', 'django_spinproject.bin']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['django-spinproject = '
                     'django_spinproject.bin.spinproject:main']}

setup_kwargs = {
    'name': 'django-spinproject',
    'version': '1.1.0',
    'description': 'Opinionated version of `startproject` with some popular third-party packages. Starter pack includes: whitenoise, django-environ, logging, GitHub Scripts to Rule Them All, basic Dockerfile and Makefile.',
    'long_description': "# django-spinproject\n\nOpinionated version of `django-admin startproject` with some popular third-party packages. Starter pack includes:\n\n* `whitenoise` for painless work with static files;\n* `settings.py` file with `django-environ` support so you can define your databases and stuff with environment variables and `.env` files;\n    * Also, mostly pre-configured (but still optional) app and SQL logging;\n    * Also, `django-postgres-readonly` (in case you have R/O databases);\n    * But otherwise, it's still your standard `settings.py` you used to see in every other project.\n* `script/bootstrap` and other [scripts to rule them all](https://github.blog/2015-06-30-scripts-to-rule-them-all/) so your fellow developers and maintainers don't ask you how to run this thing. Current versions of these scripts optimized for use with [poetry](https://python-poetry.org/), but you can easily adapt them for any Python package manager;\n* A basic `Dockerfile` (and `make` targets for its common usage patterns);\n* `make lint` command for linting with flake8.\n\n## Requirements\n\n* \\*nix system;\n* `django-admin` installed and available from `$PATH`.\n\nGenerated files will work fine in Django >= 2.0, not tested in earlier versions.\n\n## How to use\n\n1. Install the package: `pip install django-spinproject`\n2. `django-spinproject <project name> <path>`\n\nAlso, take a look at `enhance-*` scripts (parameters are the same) if you only need to add one specific thing to existing project.\n\n## Planned features\n\n(for requests, create an issue or drop me a line at m1kc@yandex.ru)\n\n* Always call the main module `main`\n* Gitlab CI config\n* pytest support\n\n## Changelog\n\n### Apr 16, 2021\n\n* `.gitignore` to keep your VCS clean;\n* `.dockerignore` to keep your Docker images clean;\n* `make clean` to get rid of `__pycache__` files when you need that;\n* No need to install `django-postgres-readonly` anymore.\n\n### Feb 5, 2021\n\n* To avoid confusion, `python3` executable is now used instead of `python`.\n\n### Feb 20, 2020\n\n* Makefile now includes an additional target, `lint`, for linting your project with `flake8`. Give it a try: `$ make lint`.\n* Dockerfile now works properly with most recent version of Poetry.\n",
    'author': 'm1kc (Max Musatov)',
    'author_email': 'm1kc@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m1kc/django-spinproject',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
