# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rundeckpy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'paramiko>=2.7.2,<3.0.0']

entry_points = \
{'console_scripts': ['rundeckpy = rundeckpy.rundeckpy:cli']}

setup_kwargs = {
    'name': 'rundeckpy',
    'version': '0.2.4',
    'description': 'Base class, template and plugins for Rundeck python plugin',
    'long_description': '=========\nrundeckpy\n=========\nPython based Rundeck plugins.\n\nThe package contains:\n\n* a command line tool\n* a series of plugins\n* squleton for new plugins\n* Base classes\n\ncommand line tool\n#################\n\n\nplugins\n#######\n\n\nsqueleton\n#########\n\n\nbase class\n##########',
    'author': 'Thiago Takayama',
    'author_email': 'thiago@takayama.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://labitup.atlassian.net/wiki/spaces/RUNPY/overview',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
