# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_sugar',
 'dbt_sugar.core',
 'dbt_sugar.core.clients',
 'dbt_sugar.core.config',
 'dbt_sugar.core.connectors',
 'dbt_sugar.core.task',
 'dbt_sugar.core.ui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.2,<2.0.0',
 'luddite>=1.0.1,<2.0.0',
 'packaging>=20.8,<21.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'pydantic>=1.8,<2.0',
 'pyfiglet>=0.8.post1,<0.9',
 'pytest-dictsdiff>=0.5.8,<0.6.0',
 'questionary>=1.9.0,<2.0.0',
 'rich>=9.13,<11.0',
 'snowflake-sqlalchemy>=1.2.4',
 'yamlloader>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['dbt-sugar = dbt_sugar.core.main:main']}

setup_kwargs = {
    'name': 'dbt-sugar',
    'version': '0.0.0rc1',
    'description': 'A sweet CLI tool to help dbt users enforce documentation and testing on their dbt projects.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/dbt-sugar.svg)](https://badge.fury.io/py/dbt-sugar)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)\n\n![Build](https://github.com/bitpicky/dbt-sugar/actions/workflows/main_ci.yml/badge.svg)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/bitpicky/dbt-sugar/main.svg)](https://results.pre-commit.ci/latest/github/bitpicky/dbt-sugar/main)\n[![codecov](https://codecov.io/gh/bitpicky/dbt-sugar/branch/main/graph/badge.svg?token=JB0E0LZDW1)](https://codecov.io/gh/bitpicky/dbt-sugar)\n[![Maintainability](https://api.codeclimate.com/v1/badges/1e6a887de605ef8e0eca/maintainability)](https://codeclimate.com/github/bitpicky/dbt-sugar/maintainability)\n\n[![Downloads](https://pepy.tech/badge/dbt-sugar)](https://pepy.tech/project/dbt-sugar)\n[![Discord](https://img.shields.io/discord/752101657218908281?label=discord)](https://discord.gg/cQB49ejbCA)\n\nDocumentation on [gitbook](https://bitpicky.gitbook.io/dbt-sugar/)\n\nIf you want to help out and join the party feel free to:\n\n- [create an issue](https://github.com/bitpicky/dbt-sugar/issues) or more fun\n- join us on [Discord](https://discord.gg/cQB49ejbCA) :sparkles: and\n- check the [ROADMAP.md](ROADMAP.md) to see what's in the plans.\n\n# dbt-sugar :candy:\n\n:warning: **dbt-sugar is pretty alpha, don't use on your prod models unless you have tested it in a safe place before.**\n\n## What is dbt-sugar?\n\ndbt-sugar is a CLI tool that allows users of [dbt](https://www.getdbt.com/) to have fun and ease performing actions around dbt models such as:\n\n- documentation\n- test enforcement\n  and probably more in a not too distant future.\n\n  We keep track of our progress in the [projects](https://github.com/bitpicky/dbt-sugar/projects) section.\n",
    'author': 'Bastien Boutonnet',
    'author_email': 'bastien.b1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bitpicky/dbt-sugar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.3,<3.10',
}


setup(**setup_kwargs)
