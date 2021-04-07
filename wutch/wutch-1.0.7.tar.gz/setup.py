# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wutch', 'wutch.js']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'aiohttp>=3.7.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'ilexconf>=0.9.5,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'watchdog>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['wutch = wutch:cli']}

setup_kwargs = {
    'name': 'wutch',
    'version': '1.0.7',
    'description': 'Watch and rebuild your files like LiveServer',
    'long_description': '# Wutch\n\n`wutch` watches for changes in the directories and runs a shell command for\nevery change. It can also open a browser a display whatever is in the build\ndirectory, just like Live Server.\n\nCommon use case for Wutch involves writing docs with [Sphinx][sphinx]. Wutch will\nwatch for the changes in all `*.rst` files and automatically rebuild documentation.\nIt will also open a browser window pointing to the build directory and inject\nevery built webpage with a code that will auto-refresh that page after each\nrebuild.\n\n<p>\n    <a href="https://pypi.org/project/wutch/"><img alt="PyPI" src="https://img.shields.io/pypi/v/wutch?color=blue&logo=pypi"></a>\n    <a href=\'https://wutch.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/wutch/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n</p>\n\n![Wutch Demo](https://github.com/vduseev/wutch/raw/master/docs/_static/wutch-demo.gif)\n\n## Installation\n\n```shell\npip install wutch\n```\n\n## Usage\n\nJust run wutch in the directory where you want to watch for the changes.\nBy default, `wutch` will:\n\n* Watch for every change in the current directory.\n* Ignore changes in the `_build/` and `build` directories.\n* Run `sphinx-build` shell command for every change in the files.\n* Open a browser pointing to `index.html` in the `_build` directory.\n* Automatically refresh that page every time you change the files\n  and shell command runs.\n\n```shell\n$ wutch\n\n2021-04-02 23:47:06.216 | DEBUG    | wutch.config:__init__:48 - Config{\'dirs\': [\'docs\'], \'ignore_dirs\': [], \'patterns\': [\'*.rst\', \'*.py\'], \'ignore_patterns\': [], \'command\': \'make -C docs rebuild\', \'build\': \'docs/_build/html\', \'inject_patterns\': [\'*.html\'], \'index\': \'index.html\', \'host\': \'localhost\', \'port\': 5010, \'wait\': 3, \'no_browser\': False, \'no_server\': False}\n2021-04-02 23:47:06.217 | DEBUG    | wutch.watcher:start:24 - Starting observer thread\n2021-04-02 23:47:06.219 | DEBUG    | wutch.watcher:start:26 - Observer thred started\n2021-04-02 23:47:06.220 | DEBUG    | wutch.server:start:44 - Server thread started\n2021-04-02 23:47:06.220 | DEBUG    | wutch.server:_open_browser:133 - Opening browser at: http://localhost:5010/index.html\n```\n\nStop wutch by issuing a <kbd>Ctrl+C</kbd> key sequence.\n\n```shell\n^C2021-04-02 23:47:25.283 | DEBUG    | wutch.threaded:run:28 - Stopping all threads on KeyboardInterrupt\n2021-04-02 23:47:25.283 | DEBUG    | wutch.watcher:stop:30 - Stopping observer thread\n2021-04-02 23:47:26.260 | DEBUG    | wutch.watcher:stop:33 - Observer thread stopped\n2021-04-02 23:47:26.260 | DEBUG    | wutch.server:stop:58 - Server thread stopped\n```\n\n## Configuration\n\n### Parameters\n\n```shell\n  -h, --help            show this help message and exit\n  -c COMMAND, --command COMMAND\n                        Shell command executed in response to file changes. Defaults to: sphinx-build.\n  -p [PATTERNS ...], --patterns [PATTERNS ...]\n                        Matches paths with these patterns (separated by \' \'). Defaults to: [\'*\'].\n  -P [IGNORE_PATTERNS ...], --ignore-patterns [IGNORE_PATTERNS ...]\n                        Ignores file changes in these patterns (separated by \' \'). Defaults to: [].\n  -d [DIRS ...], --dirs [DIRS ...]\n                        Directories to watch (separated by \' \'). Defaults to: [\'.\'].\n  -D [IGNORE_DIRS ...], --ignore-dirs [IGNORE_DIRS ...]\n                        Ignore file changes in these directories (separated by \' \'). Defaults to: [\'_build\', \'build\'].\n  -w WAIT, --wait WAIT  Wait N seconds after the command is finished before refreshing the web page. Defaults to: 3.\n  -b BUILD, --build BUILD\n                        Build directory containing files to render in the browser. Defaults to: _build.\n  -I [INJECT_PATTERNS ...], --inject-patterns [INJECT_PATTERNS ...]\n                        Patterns of files to inject with JS code that refreshes them on rebuild (separated by \' \'). Defaults to: [\'*.htm*\'].\n  -i INDEX, --index INDEX\n                        File that will be opened in the browser with the start of the watcher. Defaults to: index.html.\n  --host HOST           Host to bind internal HTTP server to. Defaults to: localhost.\n  --port PORT           TCP port to bind internal HTTP server to. Defaults to: 5010.\n  -B NO_BROWSER, --no-browser NO_BROWSER\n                        Do not open browser at wutch launch. Defaults to: False.\n  -S NO_SERVER, --no-server NO_SERVER\n                        Do not start the webserver, just launch the shell command. Defaults to: False.\n```\n\n### Loading order\n\nWutch loads configuration settings in the following priority:\n\n1. Command line arguments\n2. Environment variables starting with `WUTCH_`\n3. Configuration file `wutch.cfg`\n4. Default variables\n\nEvery variable can be specified in any of the sources above, thanks to\n[`ilexconf`][ilexconf] configuration management library.\n\nFor example, `dirs` variable that lists directories to watch can be\nspecified in several ways:\n\n**Command line:**\n\n```shell\nwutch --dirs . ../other_dir\n```\n\n**Environment variables starting with `WUTCH_`:**\n\n```shell\nexport WUTCH_DIRS=". ../other_dir"\n```\n\n**Configuration file `wutch.cfg`:**\n\n```json\n{\n    "dirs": [".", "../other_dir"]\n}\n```\n\n## Wutch\'s documentation is built using `wutch`\n\nTake a look at the `wutch.cfg` file at the root of the repository. This\nserves as a somewhat common configuration for Sphinx dependent documentation.\n\nWutch documentation is developed using `wutch` and this config below.\n\n```json\n{\n    "dirs": ["docs"],\n    "ignore_dirs": [],\n    "patterns": ["*.rst", "*.py"],\n    "ignore_patterns": [],\n    "command": "make -C docs rebuild",\n    "build": "docs/_build/html",\n    "inject_patterns": ["*.html"],\n    "index": "index.html",\n    "host": "localhost",\n    "port": 5010\n}\n```\n\n\n[sphinx]: https://www.sphinx-doc.org/ "Sphinx"\n[ilexconf]: https://github.com/ilexconf/ilexconf "Ilexconf"',
    'author': 'vduseev',
    'author_email': 'vagiz@duseev.com',
    'maintainer': 'vduseev',
    'maintainer_email': 'vagiz@duseev.com',
    'url': 'https://github.com/vduseev/wutch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
