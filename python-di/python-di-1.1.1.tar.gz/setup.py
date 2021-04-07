# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['di',
 'di.core',
 'di.core.assignment',
 'di.core.compose',
 'di.core.injection',
 'di.core.instance',
 'di.core.module',
 'di.declarative',
 'di.declarative.aggregation',
 'di.declarative.app',
 'di.declarative.element',
 'di.declarative.module',
 'di.utils',
 'di.utils.inspection',
 'di.utils.inspection.module_factories',
 'di.utils.inspection.module_variables']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-di',
    'version': '1.1.1',
    'description': 'Fully automatic dependency injection for python',
    'long_description': '# python-di\n\n[![CI](https://github.com/dlski/python-di/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/dlski/python-di/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/dlski/python-di/branch/master/graph/badge.svg?token=DXIZA2T8W6)](https://codecov.io/gh/dlski/python-di)\n[![pypi](https://img.shields.io/pypi/v/python-di.svg)](https://pypi.python.org/pypi/python-di)\n[![downloads](https://img.shields.io/pypi/dm/python-di.svg)](https://pypistats.org/packages/python-di)\n[![versions](https://img.shields.io/pypi/pyversions/python-di.svg)](https://github.com/dlski/python-di)\n[![license](https://img.shields.io/github/license/dlski/python-di.svg)](https://github.com/dlski/python-di/blob/master/LICENSE)\n\nFully automatic dependency injection for python 3.7, 3.8, 3.9, pypy3 using (not only) argument annotations / type hints.\n\nCorresponds to clean architecture patterns and ideal for business applications created in DDD / Hexagonal architecture flavour.\nNo external dependencies - uses only standard libraries.\n\nKey features:\n- automatic type matching based on type hints / type annotations - \n  no manual configuration is needed, it just works out of the box\n- configurable object aggregation injection - \n  DI can join `SomeClass` objects and inject into argument annotated as `Collection[SomeClass]`\n- not harm existing codebase - \n  no decorators, no extra metadata are needed in existing codebase to make app construction possible\n- no singletons or global DI process state -\n  app or any app components can be instantiated independently as many times as needed\n- transparency of DI process - \n  static dependency graph and injection plan is built, informative exceptions on error cases\n  (like cyclic dependency or missing elements)\n\n## Help\nComing soon...\n\n## An Example\nApplication domain located in `mod_simple.py`:\n```py\nfrom typing import List\n\n\nclass Repo:\n    def read(self) -> List[str]:\n        raise NotImplementedError\n\n\nclass DomainAction:\n    def __init__(self, repo: Repo):\n        self.repo = repo\n\n    def present(self) -> str:\n        joined = ", ".join(self.repo.read())\n        return f"Data found: {joined}"\n```\n\nApplication concretes located in `mod_simple_impl.py`:\n```py\nfrom typing import List\n\nfrom mod_simple import Repo\n\n\nclass MockupRepo(Repo):\n    def read(self) -> List[str]:\n        return ["di", "test"]\n```\n\nAutomatic application construction:\n```py\nfrom di.declarative import DeclarativeApp, DeclarativeModule, scan_factories\nimport mod_simple, mod_simple_impl\n\n\ndef main():\n    # create app definition\n    app_def = DeclarativeApp(\n        DeclarativeModule(\n            # automatically add factories from `mod_simple` and `mod_simple_impl`\n            scan_factories(mod_simple, mod_simple_impl),\n        )\n    )\n\n    # build app\n    instance = app_def.build_instance()\n\n    # get initialized `DomainAction` object\n    action, = instance.values_by_type(mod_simple.DomainAction)\n\n    # check app works\n    assert action.present() == "Data found: di, test"\n```\n\n## More examples\nMore working examples are available in `tests/di/declarative/`.\nPlease see [tests/di/declarative/test_build.py](tests/di/declarative/test_build.py) for reference.\n',
    'author': 'Damian Łukawski',
    'author_email': 'damian@lukawscy.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dlski/python-di',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
