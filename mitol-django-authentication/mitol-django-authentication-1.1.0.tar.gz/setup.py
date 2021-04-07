# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitol',
 'mitol.authentication',
 'mitol.authentication.migrations',
 'mitol.authentication.settings',
 'mitol.authentication.urls',
 'mitol.authentication.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.12,<3.2',
 'djangorestframework>=3.0.0,<4.0.0',
 'mitol-django-common>=0.7.0,<0.8.0',
 'mitol-django-mail>=1.0.0,<2.0.0',
 'python3-saml>=1.10.1,<2.0.0',
 'social-auth-app-django>=3.1.0,<4.0.0',
 'social-auth-core>=3.3.3,<4.0.0']

extras_require = \
{'dev': ['ipython>=7.13.0,<8.0.0'],
 'test': ['pytest>=4.6,<5.0',
          'pytest-cov',
          'pytest-mock==1.10.1',
          'pytest-django==3.4.8',
          'isort>=4.3.21,<5.0.0',
          'black>=19.10b0,<20.0',
          'pylint>=2.0,<3.0',
          'pylint-django>=2.0.2,<3.0.0',
          'mypy>=0.782,<0.783',
          'django-stubs==1.6.0',
          'factory_boy>=2.12.0,<3.0.0',
          'responses>=0.10.14,<0.11.0']}

setup_kwargs = {
    'name': 'mitol-django-authentication',
    'version': '1.1.0',
    'description': 'MIT Open Learning django app extensions for social-auth',
    'long_description': None,
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
