# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_numpy_random']
install_requires = \
['flake8>=3.9.0,<4.0.0']

entry_points = \
{'flake8.extension': ['NPR = flake8_numpy_random:Plugin']}

setup_kwargs = {
    'name': 'flake8-numpy-random',
    'version': '0.1.0',
    'description': 'Plugin for Flake8 that forbids usage of numpy.random()',
    'long_description': '# flake8-numpy-random\nPlugin for Flake8 that forbids usage of numpy.random()\n\n## Installation\n```bash\npip install flake8-numpy-random\n```\n\n## Error codes\n| Error code |       Description         |\n|:----------:|:-------------------------:|\n|    NPR001  | do not use numpy.random() |\n\n## License\nMIT',
    'author': 'Andrey Evtikheev',
    'author_email': 'eft000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aevtikheev/flake8-numpy-random',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
