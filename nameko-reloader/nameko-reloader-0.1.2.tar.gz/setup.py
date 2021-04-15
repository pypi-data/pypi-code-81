# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nameko_reloader']

package_data = \
{'': ['*']}

install_requires = \
['nameko>=2.13.0,<3.0.0']

entry_points = \
{'console_scripts': ['nameko_reloader = nameko_reloader.nameko_reloader:main']}

setup_kwargs = {
    'name': 'nameko-reloader',
    'version': '0.1.2',
    'description': 'Add hot reload feature for nameko services',
    'long_description': '# nameko-reloader\n\nExtension for [Nameko](https://www.nameko.io/), that implements the _hot-reload_ feature, when detects changes in service file.\n\n## Usage\n\nStart your services using `nameko_reloader`, and passing the `--reload` option:\n\n```sh\nnameko_reloader run service.service_a service.service_b --reload\n```\n',
    'author': 'Instruct Developers',
    'author_email': 'oss@instruct.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/instruct-br/nameko-reloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
