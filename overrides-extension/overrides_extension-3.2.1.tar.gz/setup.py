# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['overrides_extension']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'overrides-extension',
    'version': '3.2.1',
    'description': 'A decorator to automatically detect mismatch when overriding a method.',
    'long_description': 'overrides\n=========\n\n.. image:: https://api.travis-ci.org/mkorpela/overrides.svg\n        :target: https://travis-ci.org/mkorpela/overrides\n\n.. image:: https://coveralls.io/repos/mkorpela/overrides/badge.svg\n        :target: https://coveralls.io/r/mkorpela/overrides\n\n.. image:: https://img.shields.io/pypi/v/overrides.svg\n        :target: https://pypi.python.org/pypi/overrides\n\n.. image:: http://pepy.tech/badge/overrides\n        :target: http://pepy.tech/project/overrides\n\nA decorator to automatically detect mismatch when overriding a method.\nSee http://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method\n\nAll checks are done when a class or a method is created and *not* when a method is executed or\nan instance of a class is created. This means that performance implications are minimal.\n\n*Note:*\nVersion 2.8.0 is the last one that supports Python 2.7.\nVersions after that work with Python >= 3.6.\n\nWhy explicit overrides?\n-----------------------\n\nOverrides without explicit indicator for them are weak. They leave room for problems that happen during the evolution of a codebase.\n\n1. (create) Accidental overriding in a subclass when a method to a superclass is added (or vice versa).\n2. (modify) Rename of a superclass method without subclass method rename (or vice versa).\n3. (delete) Deleting of a superclass method without detecting in subclass that the method is not anymore overriding anything (or vice versa).\n\nThese might happen for example when overriding a method in a module that does not live in your codebase, or when merging changes done by someone else to the codebase without having access to your subclass.\n\nInstallation\n------------\n.. code-block:: bash\n\n    $ pip install git+https://github.com/mozharovsky/overrides.git\n\nUsage\n-----\n.. code-block:: python\n\n    from overrides import override\n\n\n    class SuperClass:\n        def method(self) -> int:\n            """This is the doc for a method and will be shown in subclass method too!"""\n            return 2\n\n\n    class SubClass(SuperClass):\n        @override\n        def method(self) -> int:\n            return 1\n\n\nEnforcing usage\n---------------\n\n.. code-block:: python\n\n\n    from overrides import EnforceOverrides, final, override\n\n\n    class SuperClass(EnforceOverrides):\n        @final\n        def method(self) -> int:\n            """This is the doc for a method and will be shown in subclass method too!"""\n            return 2\n\n        def method2(self) -> int:\n            """This is the doc for a method and will be shown in subclass method too!"""\n            return 2\n\n        @staticmethod\n        def method3() -> int:\n            """This is the doc for a method and will be shown in subclass method too!"""\n            return 2\n\n\n    # THIS FAILS\n    class SubClass1(SuperClass):\n        def method(self) -> int: # <-- overriding a final method\n            return 1\n\n\n    # THIS FAILS\n    class SubClass2(SuperClass):\n        def method2(self) -> int: # <-- @override decorator missing\n            return 1\n\n\n    # THIS ONE IS OK\n    class SubClass3(SuperClass):\n        @override\n        def method2(self) -> int:\n            return 1\n\n\n    # ENSURE THAT @classmethod AND @staticmethod ARE PLACED AT THE TOP\n    class SubClass4(SuperClass):\n        @staticmethod\n        @override\n        def method3() -> int:\n            return 1\n \nContributors\n------------\nThis project becomes a reality only through the work of all the people who contribute.\n\nmkorpela, drorasaf, ngoodman90, TylerYep, leeopop, donpatrice, jayvdb, joelgrus, lisyarus, soulmerge, rkr-at-dbx, mozharovsky\n',
    'author': 'Mikko Korpela',
    'author_email': 'mikko.korpela@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mozharovsky/overrides',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.0,<3.10.0',
}


setup(**setup_kwargs)
