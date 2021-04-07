# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_index']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'iscc>=1.1.0b5,<2.0.0', 'uvicorn>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['iscc-index = iscc_index.main:run_server']}

setup_kwargs = {
    'name': 'iscc-index',
    'version': '1.1.0b5',
    'description': 'ISCC Index - Nearest Neighbor Search',
    'long_description': "# iscc-index - ISCC Nearest Neighbor Search\n\n> A REST OpenAPI Backend for indexing [**ISCC codes**](https://iscc.codes) for digital media files.\n\n\nThe Webservice is build with [FastAPI](https://github.com/tiangolo/fastapi) and makes\nuse of the [ISCC reference implementation](<https://github.com/iscc/iscc-specs>).\nIt includes an interactive API documentation:\n\n![Interactive ISCC Api Docs](screenshot.jpg)\n\n\nThe Docker image is published at https://hub.docker.com/r/titusz/iscc-index\n\n\n## Install via pip\n\n```bash\n$ pip3 install iscc-index\n```\n\nStart webservice via uvicorn\n\n```bash\n$ iscc-index\nINFO:     Started server process [18800]\nINFO:     Waiting for application startup.\nINFO:     Application startup complete.\nINFO:     Uvicorn running on http://127.0.0.1:8090 (Press CTRL+C to quit)\n```\n\n## Setup for development\n\nIf you are using [poetry](https://python-poetry.org/):\n\n- After checkout cd into code directory and run 'poetry install' to install dependencies.\n- Launch dev server with: 'uvicorn iscc_index.main:app --reload' or 'icscc-index'\n- See API docs at: http://127.0.0.1:8090\n\n\n## License\n\nMIT © 2021 Titusz Pan\n",
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://iscc.codes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
