# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cfcrypt', 'cfcrypt.keyring', 'cfcrypt.rsa']

package_data = \
{'': ['*']}

install_requires = \
['cf-json>=0.1.0,<0.2.0', 'cryptography>=3.4.7,<3.5.0']

setup_kwargs = {
    'name': 'cf-crypt',
    'version': '0.1.0.dev2',
    'description': 'Encryption at rest made easy',
    'long_description': ".. Project Links\n\n     * `PYPI <https://https://pypi.org/project/cf-crypt/>`_\n     * `Documentation <https://cf-crypt.readthedocs.io/en/latest>`_\n     * `Gitlab <https://gitlab.clayfox.co.nz/keir/cf-crypt>`_\n     * `Bug Tracker <https://gitlab.clayfox.co.nz/keir/cf-crypt/-/issues>`_\n\n**Encryption at rest made easy**\n\ncf-crypt is a package to help you keep all you data resting on disk secure. It make encrypting your data at rest as easy as reading and writing from a file.\n\n.. code-block:: python\n\n\t>>> from cfcrypt import CryptFileTextIO\n\t>>> with CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key) as fh:\n\t...\t    fh.write('Super secret, secret squirrel plans.')\n\n\nInstall\n#######\n\nInstall the package from `pypi.org/project/cf-crypt <https://pypi.org/project/cf-crypt>`_ using ``pip``\n\n.. code-block:: console\n\n    $ python -m pip install cf-crypt\n    [...]\n    Successfully installed cf-crypt\n\nQuick Start\n###########\n\nGenerate Keys\n-------------\n\nThese keys are generated securely in memory.\n\nLike all in memory variables they will disappear when your script ends.\nWe really need our keys to stick around for as long as we want to decrypt our data.\n\n.. code-block:: python\n\n\t>>> from cfcrypt.rsa.key_helpers import generate_private_key\n\t>>> encryption_key = generate_private_key()\n\t>>> identity_key = generate_private_key()\n\n\nSave Keys\n---------\n\nKeys can be serialized to the PEM format and saved to disk.\n\n.. code-block:: python\n\n\t>>> from cfcrypt.rsa.key_helpers import private_key_to_pem_file\n\t>>> private_key_to_pem_file('./my_encryption_key.pem', encryption_key)\n\t>>> private_key_to_pem_file('./my_identity_key.pem', identity_key)\n\n\nThese `PEM` files are quite literally the keys to your data.\n\n\nLoad Keys\n---------\n\nIf you set a password on the `PEM` files you will need it to load them from disk.\n\n.. code-block:: python\n\n\t>>> from cfcrypt.rsa.key_helpers import pem_file_to_private_key\n\t>>> encryption_key = pem_file_to_private_key('./my_encryption_key.pem')\n\t>>> identity_key = pem_file_to_private_key('./my_identity_key.pem')\n\n\nEncrypt\n-------\n\nEncryption is really easy, just use ``CryptFileTextIO`` like a regular file interface.\n\n.. code-block:: python\n\n\t>>> from cfcrypt import CryptFileTextIO\n\t>>> with CryptFileTextIO('./my_file.crpt', 'w', encryption_key, identity_key) as fh:\n\t...\t    fh.write('Super secret, secret squirrel plans.')\n\nDecrypt\n-------\n\nDecryption is also really easy, just use ``CryptFileTextIO`` like a regular file interface.\n\n.. code-block:: python\n\n\t>>> from cfcrypt import CryptFileTextIO\n\t>>> with CryptFileTextIO('./my_file.crpt', 'r', encryption_key, identity_key) as fh:\n\t... \tdata = fh.read()\n\t>>> data\n\t'Super secret, secret squirrel plans.'\n\nMore...\n#######\n\nThere are a bunch of other useful encryption related tools in the module. See the `documentation (cf-crypt.readthedocs.io/en/latest) <https://cf-crypt.readthedocs.io/en/latest>`_ for details.\n\n * String encryption\n * Python object serialization + encryption\n * RSA signing & verification\n * File & folder encryption\n * Key management.\n\n",
    'author': 'Keir Rice',
    'author_email': 'keir@clayfox.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cf-crypt.readthedocs.io/en/latest/quickstart.html',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
