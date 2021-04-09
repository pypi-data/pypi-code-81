# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_auth', 'zemfrog_auth.jwt']

package_data = \
{'': ['*']}

install_requires = \
['zemfrog>=5.0.1,<6.0.0']

setup_kwargs = {
    'name': 'zemfrog-auth',
    'version': '1.0.3',
    'description': 'Authentication for the zemfrog framework',
    'long_description': '# zemfrog-auth\n\nAuthentication for the zemfrog framework\n\nCurrently only supports JWT (JSON Web Token) authentication.\n\n\n# Features\n\n* JWT Authentication Blueprint\n* Event signal support for user information (login, register, etc)\n\n\nUsage\n=====\n\nInstall the module\n\n```sh\npip install zemfrog-auth\n```\n\n\nAdd jwt blueprints to your zemfrog application\n\n```python\nBLUEPRINTS = ["zemfrog_auth.jwt"]\n```\n\n\nUsing event signals\n-------------------\n\nIn this section I will give an example of using the event signal using a blinker.\n\n```python\n# Add this to wsgi.py\n\nfrom zemfrog_auth.signals import on_user_logged_in\n\n@on_user_logged_in.connect\ndef on_logged_in(user):\n    print("Signal user logged in:", user)\n```\n\nFor a list of available signals, you can see it [here](https://github.com/zemfrog/zemfrog-auth/blob/main/zemfrog_auth/signals.py).\nFor signal documentation you can visit [here](https://pythonhosted.org/blinker/).\n',
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
