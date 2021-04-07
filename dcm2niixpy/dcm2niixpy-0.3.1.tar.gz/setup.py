# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dcm2niixpy']

package_data = \
{'': ['*']}

install_requires = \
['spython>=0.1.12,<0.2.0']

setup_kwargs = {
    'name': 'dcm2niixpy',
    'version': '0.3.1',
    'description': 'Python package of dcm2niix',
    'long_description': '# dcm2niixpy\n\nPython package of dcm2niix\n\n\n\n## Installation\n\n```bash\npip install dcm2niixpy\n```\n\n## License\n\n[MIT](https://github.com/Svdvoort/dcm2niixpy/blob/master/LICENSE)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Svdvoort/dcm2niixpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.9',
}


setup(**setup_kwargs)
