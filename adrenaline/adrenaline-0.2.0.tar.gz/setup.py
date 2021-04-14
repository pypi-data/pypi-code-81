# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['adrenaline', 'adrenaline._impl']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "darwin"': ['pyobjc-core>=7.1,<8.0',
                               'pyobjc-framework-Cocoa>=7.1,<8.0']}

entry_points = \
{'console_scripts': ['adrenaline = adrenaline.__main__:main']}

setup_kwargs = {
    'name': 'adrenaline',
    'version': '0.2.0',
    'description': 'Keep your OS from sleeping (supports Windows and macOS)',
    'long_description': None,
    'author': 'Tamas Nepusz',
    'author_email': 'ntamas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
