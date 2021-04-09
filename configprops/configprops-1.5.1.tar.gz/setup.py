# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configprops']

package_data = \
{'': ['*']}

install_requires = \
['prettytable>=2.1.0,<3.0.0', 'python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'configprops',
    'version': '1.5.1',
    'description': 'This package provides a configuration base class to be extended with list of KEYS (same prefix) that could be overridden by environment variables.',
    'long_description': "# configprops\n\n## Introduction\n\nThis package provides a configuration base class to be extended with list of KEYS (same prefix) that could be overridden by environment variables. \n\n## API\n\n```python\nclass ConfigurationProperties(key_name_prefix:str, dot_env:bool=False, debug=False):\n ...\n```\n\nflag `dot_env` means loading `.env` file.\n\n## Examples\n\n```python\n#!/usr/bin/env python3\n\nfrom configprops import ConfigurationProperties\nimport os\n\n\nclass AppTestConfig(ConfigurationProperties):\n    TEST_APP_CONFIG_KEY_TEXT = 'Original'\n    TEST_APP_CONFIG_KEY_BOOL = True\n    TEST_APP_CONFIG_KEY_INT = 32\n    TEST_APP_CONFIG_KEY_FLOAT = 3.3\n    TEST_APP_CONFIG_KEY_OTHER = 55\n\n\ndef test_override():\n    os.environ['TEST_APP_CONFIG_KEY_BOOL'] = '0'\n    os.environ['TEST_APP_CONFIG_KEY_FLOAT'] = '8.5'\n    os.environ['TEST_APP_CONFIG_KEY_INT'] = '185'\n\n    config = AppTestConfig('TEST_APP_CONFIG_')\n\n    assert config.TEST_APP_CONFIG_KEY_BOOL == False\n    assert config.TEST_APP_CONFIG_KEY_OTHER == 55\n    assert config.TEST_APP_CONFIG_KEY_FLOAT == 8.5\n    assert config.TEST_APP_CONFIG_KEY_INT == 185\n\n```\n",
    'author': 'Xu Yijun',
    'author_email': 'xuyijun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tommyxu/configprops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
