# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['singer_sdk',
 'singer_sdk.helpers',
 'singer_sdk.samples.sample_tap_countries',
 'singer_sdk.samples.sample_tap_gitlab',
 'singer_sdk.samples.sample_tap_google_analytics',
 'singer_sdk.streams',
 'singer_sdk.tests',
 'singer_sdk.tests.cookiecutters',
 'singer_sdk.tests.core',
 'singer_sdk.tests.external',
 'singer_sdk.tests.external_snowflake']

package_data = \
{'': ['*'],
 'singer_sdk.samples.sample_tap_countries': ['schemas/*'],
 'singer_sdk.samples.sample_tap_gitlab': ['schemas/*'],
 'singer_sdk.samples.sample_tap_google_analytics': ['resources/*', 'schemas/*'],
 'singer_sdk.tests.core': ['resources/*'],
 'singer_sdk.tests.external': ['.secrets/*'],
 'singer_sdk.tests.external_snowflake': ['.secrets/*']}

install_requires = \
['PyJWT==1.7.1',
 'backoff==1.8.0',
 'click>=7.1.2,<8.0.0',
 'cryptography>=3.4.6,<4.0.0',
 'pendulum==1.2.0',
 'pipelinewise-singer-python==1.2.0',
 'requests>=2.25.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['plugin-base = singer_sdk.plugin_base:PluginBase.cli']}

setup_kwargs = {
    'name': 'singer-sdk',
    'version': '0.1.1',
    'description': 'A framework for building Singer taps',
    'long_description': None,
    'author': 'Meltano Team and Contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
