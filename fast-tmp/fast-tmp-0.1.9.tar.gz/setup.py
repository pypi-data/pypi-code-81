# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_tmp',
 'fast_tmp.conf',
 'fast_tmp.depends',
 'fast_tmp.utils',
 'fastapi_cli',
 'fastapi_cli.tpl.app.{{cookiecutter.app_name}}',
 'fastapi_cli.tpl.app.{{cookiecutter.app_name}}.routes',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.tests',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.enums']

package_data = \
{'': ['*'],
 'fastapi_cli': ['tpl/app/*',
                 'tpl/project/*',
                 'tpl/static/*',
                 'tpl/static/static/*']}

install_requires = \
['cookiecutter>=1.7.2,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['fast-tmp = fastapi_cli:main']}

setup_kwargs = {
    'name': 'fast-tmp',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'Chise1',
    'author_email': 'chise123@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Chise1/fast-tmp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
