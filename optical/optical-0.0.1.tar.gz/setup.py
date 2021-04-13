# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optical', 'optical.converter', 'optical.visualizer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'altair>=4.1.0,<5.0.0',
 'bounding-box>=0.1.3,<0.2.0',
 'joblib>=1.0.1,<2.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'mediapy>=0.2.2,<0.3.0',
 'pandas>=1.2.3,<2.0.0',
 'tqdm>=4.59.0,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=3.5.3,<4.0.0',
          'sphinx-panels>=0.5.2,<0.6.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0']}

setup_kwargs = {
    'name': 'optical',
    'version': '0.0.1',
    'description': 'Utilities for vision related tasks',
    'long_description': '# Optical\n\n\n<p align="center"><img align="centre" src="assets/optical_b.png" alt="logo" width = "650"></p>\n\nA collection of utilities for ML vision related tasks.\n\n## Contributing\n\n1. clone the repo\n2. install poetry:\n    ```sh\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -\n    ```\n\n### Work inside the dev container (recommended):\n3. Open the project in Visual Studio Code. in the status bar, select open in remote container.\n\nNote: You would require Visual Studio Code installed in your system and Docker desktop client running in order to use this option. Additionally you would require to install "Remote Container" extension for VScode.\n\n### Work in local environment:\n\n3. work on virtual environment:\n   ```sh\n   conda create -n optical python=3.8 pip\n   ```\n\n4. install the dependencies and the project in editable mode\n   ```sh\n   poetry install\n   ```\n\nNote: Do not forget to work on branches.\n',
    'author': 'Bishwarup B',
    'author_email': 'write2bishwarup@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hashtagml/optical',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
