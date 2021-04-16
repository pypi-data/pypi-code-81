# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wkconnect',
 'wkconnect.backends',
 'wkconnect.backends.boss',
 'wkconnect.backends.neuroglancer',
 'wkconnect.backends.tiff',
 'wkconnect.backends.wkw',
 'wkconnect.routes',
 'wkconnect.routes.datasets',
 'wkconnect.utils',
 'wkconnect.webknossos']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=6.2,<7.0',
 'aiohttp>=3.7,<4.0',
 'async-lru>=1.0,<2.0',
 'blosc>=1.10,<2.0',
 'brotlipy>=0.7.0,<0.8.0',
 'compressed_segmentation>=1.0,<2.0',
 'gcloud-aio-auth>=3.0,<4.0',
 'jpeg4py>=0.1.4,<0.2.0',
 'numpy>=1.17,<2.0',
 'sanic==18.12.0',
 'sanic_cors>=0.9.9,<0.10.0',
 'tifffile>=2020.9.3,<2021.0.0',
 'wkcuber>=0.5,<0.6']

setup_kwargs = {
    'name': 'wkconnect',
    'version': '21.4.0',
    'description': '',
    'long_description': None,
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
