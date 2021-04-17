# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_settings']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coveo-settings',
    'version': '1.0.5',
    'description': 'Settings driven by environment variables.',
    'long_description': '# coveo-settings\n\nWhenever you want the user to be able to configure something through an environment variable, this module has your back:\n\n```python\nfrom coveo_settings.settings import StringSetting, BoolSetting\n\nDATABASE_URL = StringSetting(\'project.database.url\')\nDATABASE_USE_SSL = BoolSetting(\'project.database.ssl\')\n```\n\nThe user can then configure the environment variables `project.database.url` and `project.database.ssl` to configure the application.\n\nWhen accessed, the values are automatically converted to the desired type:\n\n- `StringSetting` will always be a string\n- `BoolSetting` is either True or False, but accepts "yes|no|true|false|1|0" as input (case-insensitive, of course)\n- `IntSetting` and `FloatSetting` are self-explanatory\n- `DictSetting` allows you to use JSON maps\n\nIf the input cannot be converted to the value type, an `InvalidConfiguration` exception is raised.\n\nA default (fallback) value may be specified. The fallback may be a `callable`.\n\n\n## Accessing the value\n\nThere are various ways to obtain the value:\n\n```python\nfrom coveo_settings.settings import StringSetting, BoolSetting\n\nDATABASE_USE_SSL = BoolSetting(\'project.database.ssl\')\n\n# this method will raise an exception if the setting has no value and no fallback\nuse_ssl = bool(DATABASE_USE_SSL)\nassert use_ssl in [True, False]\n\n# this method will not raise an exception\nuse_ssl = DATABASE_USE_SSL.value\nassert use_ssl in [True, False, None]\n\n# use "is_set" as a shorthand for "value is not None": \nif DATABASE_USE_SSL.is_set:\n    use_ssl = bool(DATABASE_USE_SSL)\n```\n\n\n## Loose environment key matching\n\nMatching the key of the environment variable `project.database.ssl` is done very loosely:\n\n- case-insensitive\n- dots and underscores are ignored completely (`foo_bar` and `f__ooba.r` are equal)\n    - useful for some runners that don\'t support dots in environment variable keys\n    \n\n## Mocking\n\nWhen you need a setting value for a test, use the `mock_config_value` context manager:\n\n```python\nfrom coveo_settings.settings import mock_config_value, StringSetting\n\nSETTING = StringSetting(...)\n\nassert not SETTING.is_set\nwith mock_config_value(SETTING, \'new-value\'):\n    assert SETTING.is_set\n```\n\nYou can also clear the value:\n\n```python\nfrom coveo_settings.settings import mock_config_value, StringSetting\n\nSETTING = StringSetting(..., fallback=\'test\')\n\nassert SETTING.is_set\nwith mock_config_value(SETTING, None):\n    assert not SETTING.is_set\n```\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
