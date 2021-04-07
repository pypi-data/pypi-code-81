# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_inspector', 'http_inspector.logger']

package_data = \
{'': ['*']}

install_requires = \
['rich>=10.0.1,<11.0.0']

entry_points = \
{'console_scripts': ['hyper = http_inspector.__main__:main']}

setup_kwargs = {
    'name': 'hyper-inspector',
    'version': '0.0.3',
    'description': 'A simple HTTP inspector to debug webhooks and other incoming requests',
    'long_description': "A dummy/mocking server to inspect incoming HTTP connections. Use it to test/debug Webhooks.\n\n### Installation\n\nUsing `pip`:\n\n```bash\n$ pip install hyper-inspector\n```\n\nUsing `pipx`:\n\n```bash\n$ pipx install hyper-inspector\n```\n\n### Usage\n\n```\n$ hyper --help\nusage: http_inspector [-h] [-r RESPONSE] [-f [ENABLE_FILE_LOGGING]] [-d LOGGING_DIRECTORY] [--log-body [LOG_BODY]] [--ip IP] [--port PORT]\n\nInspect and debug HTTP requests\n\noptional arguments:\n  -h, --help\n            Show this help message and exit\n  -r, --response [default 200]\n            Default response for every incoming request\n  -f, --enable-file-logging [default True]\n            Enable file logging\n  -d, --logging-directory [default .]\n            Directory path to store logs\n  --log-body [default True]\n            Should it log the whole body to the console.\n  --ip [default '']\n            IP Addr to serve\n  --port [default 555]\n            Server Port to listen to\n```\n",
    'author': 'Santiago Basulto',
    'author_email': 'santiago.basulto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
