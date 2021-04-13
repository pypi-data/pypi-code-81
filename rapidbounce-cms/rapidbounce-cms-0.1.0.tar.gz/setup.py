# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rapidbounce_cms', 'rapidbounce_cms.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0',
 'django-ckeditor',
 'django-crispy-forms',
 'django-filer',
 'django-htmlmin',
 'django-imagekit',
 'django-modeltranslation',
 'django-mptt',
 'django-mptt-admin',
 'django-recaptcha',
 'django-reversion',
 'django-storages[google]==1.9.1',
 'django_compressor',
 'pillow']

setup_kwargs = {
    'name': 'rapidbounce-cms',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
