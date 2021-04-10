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
    'version': '0.0.5',
    'description': 'A simple HTTP inspector to debug webhooks and other incoming requests',
    'long_description': 'A dummy/mocking server to inspect incoming HTTP connections. Use it to test/debug Webhooks. Provides nice console logging + a dump of every request as a file.\n\n<p align="center">\n  <img width="900px" src="https://user-images.githubusercontent.com/872296/114039073-cf749480-9858-11eb-8db9-981f18b9d12c.gif">\n</p>\n\n```bash\n$ docker run -it -p 5555:5555 -v $(pwd)/logs:/app santiagobasulto/hyper\n```\n\nExplanation:\n* `-p P1:5555`, `P1` is the local port in your host.\n* `-v YOUR_PATH:/app`, `YOUR_PATH` is a volume in your file system to store the logs of the requests.\n\nLogs names have the convention `METHOD.PATH.TIMESTAMP.request.json` and `METHOD.PATH.TIMESTAMP.body.EXTENSION` (if a body is sent). For example, `POST.some.path.1617889344.request.json` and `POST.some.path.1617889344.body.json`\n\nIf you don\'t want to store the logs, don\'t pass a `-v` option.\n\n### Installation\n\nUsing `pip`:\n\n```bash\n$ pip install hyper-inspector\n```\n\nUsing `pipx`:\n\n```bash\n$ pipx install hyper-inspector\n```\n\n### Usage\n\n```\n$ hyper --help\nusage: http_inspector [-h] [-r RESPONSE] [-f [ENABLE_FILE_LOGGING]] [-d LOGGING_DIRECTORY] [--log-body [LOG_BODY]] [--ip IP] [--port PORT]\n\nInspect and debug HTTP requests\n\noptional arguments:\n  -h, --help\n            Show this help message and exit\n  -r, --response [default 200]\n            Default response for every incoming request\n  -f, --enable-file-logging [default True]\n            Enable file logging\n  -d, --logging-directory [default .]\n            Directory path to store logs\n  --log-body [default True]\n            Should it log the whole body to the console.\n  --ip [default \'\']\n            IP Addr to serve\n  --port [default 555]\n            Server Port to listen to\n```\n\n',
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
