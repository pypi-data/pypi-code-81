# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alastria_identity',
 'alastria_identity.examples',
 'alastria_identity.services',
 'alastria_identity.tests',
 'alastria_identity.types']

package_data = \
{'': ['*']}

install_requires = \
['ecdsa>=0.16.1,<0.17.0',
 'eth_abi>=2.1.1,<3.0.0',
 'jwcrypto>=0.8,<0.9',
 'mock>=4.0.2,<5.0.0',
 'pytest>=6.1.1,<7.0.0',
 'requests>=2.24.0,<3.0.0',
 'web3>=5.13.0,<6.0.0']

setup_kwargs = {
    'name': 'alastria-identity',
    'version': '0.2.0',
    'description': '',
    'long_description': '# alastria-identity-lib-py\n\nPython version of the Alastria Identity lib\n\n# Testing\n\nExecute tests\n```bash\ndocker-compose run --rm identity poetry run python -m coverage run -m pytest alastria_identity -v .\n```\n\nCreate and check test coverage\n```bash\ndocker-compose run --rm identity poetry run coverage html\nnpx http-server (or any local http server)\n```\n\nOpen `http://localhost:8080` in your browser\n\n# TODO\n\n- This README\n- Add more code examples\n- Create the PyPI package and push it to pypi.org\n- Test the connection with the identity Alastria network node\n- Delegate calls is still a WIP, we need to finish that\n',
    'author': 'Javier Aguirre',
    'author_email': 'javi@wealize.digital',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Wealize/alastria-identity-lib-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
