# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongomantic', 'mongomantic.core']

package_data = \
{'': ['*']}

install_requires = \
['bson>=0.5.10,<0.6.0',
 'pydantic>=1.8.1,<2.0.0',
 'pymongo>=3.11.3,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.8.2,<10.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'wily>=1.19.0,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['mongomantic = mongomantic.__main__:app']}

setup_kwargs = {
    'name': 'mongomantic',
    'version': '0.2.0',
    'description': 'A MongoDB Python ORM, built on Pydantic and PyMongo.',
    'long_description': '![Logo](https://github.com/RamiAwar/mongomantic/blob/main/docs/assets/text_logo.png)\n\n<p align="center">\n    <em>Mongomantic = Pymongo + <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a></em>\n</p>\n<p>Mongomantic is an easy-to-use, easy-to-learn wrapper around PyMongo, built around <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a> models.</p>\n\n<div align="center">\n\n[![Build status](https://github.com/RamiAwar/mongomantic/workflows/build/badge.svg?branch=main&event=push)](https://github.com/RamiAwar/mongomantic/actions?query=workflow%3Abuild)\n\n<!-- [![Python Version](https://img.shields.io/pypi/pyversions/mongomantic.svg)](https://pypi.org/project/mongomantic/)-->\n\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/RamiAwar/mongomantic/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/RamiAwar/mongomantic/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/RamiAwar/mongomantic/releases)\n[![License](https://img.shields.io/github/license/RamiAwar/mongomantic)](https://github.com/RamiAwar/mongomantic/blob/main/LICENSE)\n\nA lightweight MongoDB ORM based on Pydantic and PyMongo, heavily inspired by Mongoengine.\n\n</div>\n\n## API\n\n```python\nfrom mongomantic import BaseRepository, MongoDBModel\n\n\nclass User(MongoDBModel):\n    first_name: str\n    last_name: str\n\nclass UserRepository(BaseRepository):\n    @property\n    def _model(self):  # Define model type\n        return User\n\n    @property\n    def _collection(self):  # Define collection name\n        return "user"\n\nuser = User(first_name="John", last_name="Smith")\nuser_repo = UserRepository()\n\nuser = user_repo.save(user)\nuser.id  # ObjectId that was saved\n\n```\n\n## Your Opinion is Needed\n\nMongomantic can be kept as a simple wrapper around PyMongo, or developed into a miniature version of Mongoengine that\'s built on Pydantic.\nThe first direction would result in the following API:\n\n```\n# Direct pymongo wrapper\nusers = user_repo.find({"$and": [{"age": {"$gt": 12}}, {"name": "John"}]})\n\n# But matches can be done as keyword arguments\njohn = user_repo.find(name="John")\n```\n\nOn the other hand, a more complex version of Mongomantic could lead to:\n\n```\n# More Pythonic way of writing queries\nusers = user_repo.find(User.age > 12, name="John")\n\n# Matches still compact\njohn = user_repo.find(name="John")\n```\n\nPlease submit your vote below.\n\n<p><a href="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/Simple%20PyMongo%20Wrapper%20-%20Prefer%20speed%20and%20native%20mongodb%20filters/vote"><img src="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/Simple%20PyMongo%20Wrapper%20-%20Prefer%20speed%20and%20native%20mongodb%20filters" alt="">Simple PyMongo Wrapper - Prefer speed and native mongodb filters</a>\n<a href="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/More%20Complex%20Wrapper%20-%20Pythonic%20filters/vote"><img src="https://api.gh-polls.com/poll/01F2Y55FJSGXFMJW97Z143C6E0/More%20Complex%20Wrapper%20-%20Pythonic%20filters" alt="">More Complex Wrapper - Pythonic Filters</a></p>\n\n\n## 🚀 TODO\n\n- [ ] Documentation\n- [x] Basic API similar to mongoengine, without any queryset logic\n- [x] Built on Pydantic models, no other schema required\n- [x] BaseRepository responsible for all operations (instead of the model itself)\n- [ ] ProductionRepository derived from BaseRepository with all errors handled\n- [ ] Repository/model plugin framework (ex. SyncablePlugin, TimestampedPlugin, etc.)\n- [ ] Wrapper for aggregation pipelines\n- [x] Mongomock tests\n- [ ] Flexible connect() function wrapper around PyMongo client (aliases, replica sets, retry writes, etc.)\n- [ ] Clean up imports and expose essentials in main file\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/RamiAwar/mongomantic)](https://github.com/RamiAwar/mongomantic/blob/main/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/RamiAwar/mongomantic/blob/main/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{mongomantic,\n  author = {mongomantic},\n  title = {A MongoDB Python ORM, built on Pydantic and PyMongo.},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/RamiAwar/mongomantic}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'mongomantic',
    'author_email': 'rami@hyperchess.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RamiAwar/mongomantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
