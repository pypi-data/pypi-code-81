# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3manifestcollectstatic',
 's3manifestcollectstatic.management',
 's3manifestcollectstatic.management.commands']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 's3manifestcollectstatic',
    'version': '0.1.0',
    'description': 'Optimized collectstatic for S3ManifestStaticStorage',
    'long_description': None,
    'author': 'Daniel Dương',
    'author_email': 'daniel.duong@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
