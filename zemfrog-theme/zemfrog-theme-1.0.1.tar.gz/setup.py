# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_theme']

package_data = \
{'': ['*']}

install_requires = \
['zemfrog>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'zemfrog-theme',
    'version': '1.0.1',
    'description': 'Zemfrog theme - to register your own theme template!',
    'long_description': '# zemfrog-theme\n\nZemfrog theme - to register your own theme template!\nThe main idea is to make a template for a theme that is easy to customize.\n\n\n# Usage\n\nInstall this\n\n```sh\npip install zemfrog-theme\n```\n\nAdd this to the `EXTENSIONS` configuration\n\n```python\nEXTENSIONS = ["zemfrog_theme"]\n```\n\nAnd you can register your own theme via the `ZEMFROG_THEMES` configuration.\n\nSee boilerplate for theme creation here https://github.com/aprilahijriyan/zemfrog-theme-template\nSee sample themes here https://github.com/zemfrog/zemfrog-quasar\n',
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
