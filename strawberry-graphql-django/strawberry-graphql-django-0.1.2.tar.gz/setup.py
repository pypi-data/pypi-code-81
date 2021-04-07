# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django',
 'strawberry_django.mutations',
 'strawberry_django.queries']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0', 'strawberry-graphql>=0.53']

setup_kwargs = {
    'name': 'strawberry-graphql-django',
    'version': '0.1.2',
    'description': 'Strawberry GraphQL Django extension',
    'long_description': '# Strawberry GraphQL Django extension\n\n[![CI](https://github.com/la4de/strawberry-graphql-django/actions/workflows/main.yml/badge.svg)](https://github.com/la4de/strawberry-graphql-django/actions/workflows/main.yml)\n[![PyPI](https://img.shields.io/pypi/v/strawberry-graphql-django)](https://pypi.org/project/strawberry-graphql-django/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/strawberry-graphql-django)](https://pypi.org/project/strawberry-graphql-django/)\n\nThis library provides helpers to generate types, mutations and resolvers for Django models.\n\n> NOTE: Package v0.1.0 introduced new API. See more detailed description about new API from [the ticket](https://github.com/strawberry-graphql/strawberry-graphql-django/issues/10). Old version is still available in [v0.0.x](https://github.com/strawberry-graphql/strawberry-graphql-django/tree/v0.0.x) branch.\n\nInstalling strawberry-graphql-django packet from the python package repository.\n```shell\npip install strawberry-graphql-django\n```\n\n\n## Example project files\n\nSee example Django project [examples/django](https://github.com/strawberry-graphql/strawberry-graphql-django/tree/main/examples/django).\n\nmodels.py\n```python\nfrom django.db import models\n\nclass User(models.Model):\n    name = models.CharField(max_length=50)\n    groups = models.ManyToManyField(\'Group\', related_name=\'users\')\n\nclass Group(models.Model):\n    name = models.CharField(max_length=50)\n```\n\ntypes.py\n```python\nimport strawberry\nimport strawberry_django\nfrom . import models\n\n# model types are collected into register. type converters use\n# register to resolve types of relation fields\ntypes = strawberry_django.TypeRegister()\n\n@types.register\n@strawberry_django.type(models.User, types=types)\nclass User:\n    # types can be extended with own fields and resolvers\n    @strawberry.field\n    def name_upper(root) -> str:\n        return root.name.upper()\n\n@types.register\n@strawberry_django.type(models.Group, fields=[\'id\'], types=types)\nclass Group:\n    # fields can be remapped\n    group_name: str = strawberry_django.field(field_name=\'name\')\n\n@types.register\n@strawberry_django.input(models.User)\nclass UserInput:\n    pass\n```\n\nschema.py\n```python\nimport strawberry, strawberry_django\nfrom . import models\nfrom .types import types\n\nQuery = strawberry_django.queries(models.User, models.Group, types=types)\nMutation = strawberry_django.mutations(models.User, types=types)\nschema = strawberry.Schema(query=Query, mutation=Mutation)\n```\n\nurls.py\n```python\nfrom django.urls import include, path\nfrom strawberry.django.views import AsyncGraphQLView\nfrom .schema import schema\n\nurlpatterns = [\n    path(\'graphql\', AsyncGraphQLView.as_view(schema=schema)),\n]\n```\n\nNow we have models, types, schema and graphql view. It is time to crete database and start development server.\n```shell\nmanage.py makemigrations\nmanage.py migrate\nmanage.py runserver\n```\n\n## Mutations and Queries\n\nOnce the server is running you can open your browser to http://localhost:8000/graphql and start testing auto generated queries and mutations.\n\nCreate new user.\n```\nmutation {\n  createUsers(data: { name: "my user" }) {\n    id\n  }\n}\n```\n\nMake first queries.\n```\nquery {\n  user(id: 1) {\n    name\n    groups {\n      groupName\n    }\n  }\n  users(filters: ["name__contains=\'my\'"]) {\n    id\n    name\n    nameUpper\n  }\n}\n```\n\nUpdate user data.\n```\nmutation {\n  updateUsers(data: {name: "new name"}, filters: ["id=1"]) {\n    id\n    name\n  }\n}\n```\n\nFinally delete user.\n```\nmutation {\n  deleteUsers(filters: ["id=1"])\n}\n```\n\n## Django authentication examples\n\n`strawberry_django` provides mutations for authentications.\n\nschema.py:\n```\nclass IsAuthenticated(strawberry.BasePermission):\n    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:\n        self.message = "Not authenticated"\n        return info.context.request.user.is_authenticated\n\n@strawberry.type\nclass Query:\n    @strawberry.field(permission_classes=[IsAuthenticated])\n    def current_user(self, info: Info) -> types.User:\n        return info.context.request.user\n\nschema = strawberry.Schema(query=Query, mutation=strawberry_django.AuthMutation)\n```\n\nLogin and logout with:\n```\nmutation {\n  login(username:"myuser", password:"mypassword")\n  logout()\n}\n```\n\nGet current user with:\n```\nquery {\n  currentUser {\n    id\n    firstName\n    lastName\n  }\n}\n```\n\n## Running unit tests\n```\npoetry install\npoetry run pytest\n```\n\n## Contributing\n\nI would be more than happy to get pull requests, improvement ideas and feedback from you.\n',
    'author': 'Lauri Hintsala',
    'author_email': 'lauri.hintsala@verkkopaja.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/strawberry-graphql/strawberry-graphql-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
