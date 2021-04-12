# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depcheck']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'pydeps>=1.9.13,<2.0.0']

entry_points = \
{'console_scripts': ['depcheck = depcheck.main:main']}

setup_kwargs = {
    'name': 'depcheck',
    'version': '0.1.0',
    'description': 'Depcheck is a tool to check package dependencies between predefined layers to make sure that the application always complies with the Hexagonal Architecture principle of creating loosely coupled application components.',
    'long_description': '![Depcheck: Dependency Checker](/docs/.img/depcheck_logo.jpg)\n\n[![pipeline status](https://git.flix.tech/network/optimization/depcheck/badges/master/pipeline.svg)](https://git.flix.tech/network/optimization/depcheck/-/commits/master)\n\nDepcheck is a tool to check package-dependencies between predefined layers. In the configuration file(`.depcheck.yml`) located in the project root, which packages belong to which layers and allowed dependencies between layers are configurable. In this way, you can make sure that the application always complies with the <a href="https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)">Hexagonal Architecture</a> principle of creating loosely coupled application components.\n\n## Usage\nLet\'s say you have a project with the directory structure below:\n```text\nproject_directory\n    root_package\n        package-1\n        package-2\n        main.py\n    README.md\n    .gitignore\n    .depcheck.yml\n```\n- Navigate to the `project_directory` then run `depcheck` for your project:\n    ```shell\n    depcheck root_package\n    ```\n- As you can see in the directory structure above, we have `.depcheck.yml` configuration file in the project directory. If you would like to change the path of the configuration file, use `-f` or `--file` argument:\n    ```shell\n    depcheck root_package -f config/customized_depcheck.yml\n    ```\n',
    'author': 'FlixMobility Tech',
    'author_email': 'open-source@flixbus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flix-tech/depcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
