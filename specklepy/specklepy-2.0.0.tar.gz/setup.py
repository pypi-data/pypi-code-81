# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['specklepy',
 'specklepy.api',
 'specklepy.api.resources',
 'specklepy.logging',
 'specklepy.objects',
 'specklepy.serialization',
 'specklepy.transports',
 'specklepy.transports.server']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'gql>=3.0.0a5,<4.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'specklepy',
    'version': '2.0.0',
    'description': 'The Python SDK for Speckle 2.0',
    'long_description': '# speckle-py 🥧\n\n[![Twitter Follow](https://img.shields.io/twitter/follow/SpeckleSystems?style=social)](https://twitter.com/SpeckleSystems) [![Community forum users](https://img.shields.io/discourse/users?server=https%3A%2F%2Fdiscourse.speckle.works&style=flat-square&logo=discourse&logoColor=white)](https://discourse.speckle.works) [![website](https://img.shields.io/badge/https://-speckle.systems-royalblue?style=flat-square)](https://speckle.systems) [![docs](https://img.shields.io/badge/docs-speckle.guide-orange?style=flat-square&logo=read-the-docs&logoColor=white)](https://speckle.guide/dev/)\n\n## Introduction\n\n> ⚠ This is the start of the Python client for Speckle 2.0. It is currently quite nebulous and may be trashed and rebuilt at any moment! It is compatible with Python 3.6+ ⚠\n> \n\n## Documentation\n\nComprehensive developer and user documentation can be found in our:\n\n#### 📚 [Speckle Docs website](https://speckle.guide/dev/)\n\n## Developing & Debugging\nThis project uses python-poetry for dependency management, make sure you follow the official [docs](https://python-poetry.org/docs/#installation) to get poetry.\n\nTo bootstrap the project environment run `$ poetry install`. This will create a new virtual-env for the project and install both the package and dev dependencies.\n\nIf this is your first time using poetry and you\'re used to creating your venvs within the project directory, run `poetry config virtualenvs.in-project true` to configure poetry to do the same.\n\nTo execute any python script run `$ poetry run python my_script.py`\n\n> Alternatively you may roll your own virtual-env with either venv, virtualenv, pyenv-virtualenv etc. Poetry will play along an recognize if it is invoked from inside a virtual environment.\n\n## Overview of functionality \n\nThe `SpeckleClient` is the entry point for interacting with the GraphQL API. You\'ll need to have a running server to use this.\n\n```py\nfrom specklepy.api.client import SpeckleClient\nfrom specklepy.api.credentials import get_default_account, get_local_accounts\n\nall_accounts = get_local_accounts() # get back a list\naccount = get_default_account()\n\nclient = SpeckleClient(host="localhost:3000", use_ssl=False)\n# client = SpeckleClient(host="yourserver.com") or whatever your host is\n\nclient.authenticate(account.token)\n```\n\nInteracting with streams is meant to be intuitive and evocative of PySpeckle 1.0\n\n```py\n# get your streams\nstream_list = client.stream.list()\n\n# search your streams\nresults = client.user.search("mech")\n\n# create a stream\nnew_stream_id = client.stream.create(name="a shiny new stream")\n\n# get a stream\nnew_stream = client.stream.get(id=new_stream_id)\n```\n\nNew in 2.0: commits! Here are some basic commit interactions.\n\n```py\n# get list of commits\ncommits = client.commit.list("stream id")\n\n# get a specific commit\ncommit = client.commit.get("stream id", "commit id")\n\n# create a commit\ncommit_id = client.commit.create("stream id", "object id", "this is a commit message to describe the commit")\n\n# delete a commit\ndeleted = client.commit.delete("stream id", "commit id")\n```\n\nThe `BaseObjectSerializer` is used for decomposing and serializing `Base` objects so they can be sent / received to the server. You can use it directly to get the id (hash) and a serializable object representation of the decomposed `Base`. You can learn more about the Speckle `Base` object [here](https://discourse.speckle.works/t/core-2-0-the-base-object/782) and the decomposition API [here](https://discourse.speckle.works/t/core-2-0-decomposition-api/911).\n\n```py\nfrom specklepy.objects.base import Base\nfrom specklepy.serialization.base_object_serializer import BaseObjectSerializer\n\ndetached_base = Base()\ndetached_base.name = "this will get detached"\n\nbase_obj = Base()\nbase_obj.name = "my base"\nbase_obj["@nested"] = detached_base\n\nserializer = BaseObjectSerializer()\nhash, obj_dict = serializer.traverse_base(base_obj)\n```\n\nIf you use the `operations`, you will not need to interact with the serializer directly as this will be taken care of for you. You will just need to provide a transport to indicate where the objects should be sent / received from. At the moment, just the `MemoryTransport` and the `ServerTransport` are fully functional at the moment. If you\'d like to learn more about Transports in Speckle 2.0, have a look [here](https://discourse.speckle.works/t/core-2-0-transports/919).\n\n```py\nfrom specklepy.transports.memory import MemoryTransport\nfrom specklepy.api import operations\n\ntransport = MemoryTransport()\n\n# this serialises the object and sends it to the transport\nhash = operations.send(base=base_obj, transports=[transport])\n\n# if the object had detached objects, you can see these as well\nsaved_objects = transport.objects # a dict with the obj hash as the key\n\n# this receives and object from the given transport, deserialises it, and recomposes it into a base object\nreceived_base = operations.receive(obj_id=hash, remote_transport=transport)\n```\n\nYou can also use the GraphQL API to send and receive objects.\n\n```py\n# create a test base object\ntest_base = Base()\ntest_base.testing = "a test base obj"\n\n# run it through the serialiser\ns = BaseObjectSerializer()\nhash, obj = s.traverse_base(test_base)\n\n# send it to the server\nobjCreate = client.object.create(stream_id="stream id", objects=[obj])\n\nreceived_base = client.object.get("stream id", hash)\n```\n\nThis doc is not complete - there\'s more to see so have a dive into the code and play around! Please feel free to provide feedback, submit issues, or discuss new features ✨\n\n## Contributing\n\nPlease make sure you read the [contribution guidelines](.github/CONTRIBUTING.md) for an overview of the best practices we try to follow.\n\n## Community\n\nThe Speckle Community hangs out on [the forum](https://discourse.speckle.works), do join and introduce yourself & feel free to ask us questions!\n\n## License\n\nUnless otherwise described, the code in this repository is licensed under the Apache-2.0 License. Please note that some modules, extensions or code herein might be otherwise licensed. This is indicated either in the root of the containing folder under a different license file, or in the respective file\'s header. If you have any questions, don\'t hesitate to get in touch with us via [email](mailto:hello@speckle.systems).\n',
    'author': 'Speckle Systems',
    'author_email': 'devops@speckle.systems',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://speckle.systems/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
