# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_test', 'zemfrog_test.templates', 'zemfrog_test.templates.tests']

package_data = \
{'': ['*'], 'zemfrog_test.templates.tests': ['apis/*', 'blueprints/*']}

install_requires = \
['pytest>=6.2.2,<7.0.0', 'zemfrog>=5.0.1,<6.0.0']

entry_points = \
{'pytest11': ['zemfrog_test = zemfrog_test.fixtures']}

setup_kwargs = {
    'name': 'zemfrog-test',
    'version': '1.0.3',
    'description': 'Zemfrog unit testing tools',
    'long_description': '# zemfrog-test\nZemfrog unit testing tools\n\n# Features\n\n* Support automatically create unit tests for API / blueprints\n* Available fixtures:\n    - client\n        > This is to access the Client class to interact with the API\n    - app_ctx\n        > This is to enable the flask context application\n    - req_ctx\n        > This is to activate the flask request context application\n    - user\n        > This is to generate confirmed random users\n\n\n# Warning\n\nzemfrog test is available a finalizer to delete all users when the test session ends. so you need to create a special database for testing.\n\n\n# Usage\n\nInstall this\n\n```sh\npip install zemfrog-test\n```\n\nAnd add it to the `COMMANDS` configuration in the zemfrog application.\n\n```python\nCOMMANDS = ["zemfrog_test"]\n```\n\nNow that you have the `test` command, here is a list of supported commands:\n\n* `init` - Initialize the tests directory in the project directory.\n* `new` - Create unit tests for the API or blueprint. (The names entered must match `APIS` and `BLUEPRINTS` configurations. For example `zemfrog_auth.jwt`)\n* `run` - To run unit tests. **It doesn\'t work with the `pytest` command, don\'t know why. :/**\n',
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
