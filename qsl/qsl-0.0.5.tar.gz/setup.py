# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qsl', 'qsl.testing', 'qsl.types']

package_data = \
{'': ['*'],
 'qsl': ['frontend/*',
         'frontend/static/css/*',
         'frontend/static/js/*',
         'frontend/static/media/*'],
 'qsl.testing': ['data/*']}

install_requires = \
['Authlib>=0.15.3,<0.16.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'aiofiles',
 'async-exit-stack>=1.0.1,<2.0.0',
 'async_generator>=1.10,<2.0',
 'boto3>=1.17.15,<2.0.0',
 'click',
 'fastapi',
 'filetype>=1.0.7,<2.0.0',
 'httpx>=0.17.0,<0.18.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'uvicorn[standard]>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['qsl = qsl.cli:cli']}

setup_kwargs = {
    'name': 'qsl',
    'version': '0.0.5',
    'description': 'Yet another data labeling tool',
    'long_description': '# QSL: Quick and Simple Labeler\n\nQSL is a simple image labeling tool. It supports batch and single image labeling using images stored locally, on the web, or in cloud storage (currently only S3).\n\n## Getting Started\n\nDocumentation for more advanced functions is forthcoming, but the following will get you started with basic labeling tasks.\n\n1. Install using `pip install qsl`\n2. Start the labeling application from a desired working directory using `qsl label --port <PORT>`. The application will be running at `http://localhost:<PORT>`.\n3. Create your first labeling project, configure the labeling task with your desired classes, add images, and then start labeling in single image or batch mode.\n4. Export labels for your project in JSON format.\n\n# Development\n\n1. Install Poetry.\n2. Clone this repository.\n3. Initialize your development environment using `make init`\n4. Launch a live reloading version of the frontend and backend using `make develop`.\n',
    'author': 'Fausto Morales',
    'author_email': 'faustomorales@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/faustomorales/qsl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
