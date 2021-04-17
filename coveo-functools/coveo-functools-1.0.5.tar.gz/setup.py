# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_functools']

package_data = \
{'': ['*']}

install_requires = \
['inflection', 'typing_extensions']

setup_kwargs = {
    'name': 'coveo-functools',
    'version': '1.0.5',
    'description': 'Generic function tooling helpers',
    'long_description': '# coveo-functools\n\nIntrospection, finalizers, delegates, dispatchers, waiters...\nThese utilities aim at increasing productivity.\n\n\n## annotation\n\nIntrospect classes and callables at runtime.\n\nCan convert string annotations into their actual type reference.\n\n\n## casing / flexcase\n\nFlexcase takes a "dirty" input and maps it to a python construct.\n\nThe principal use case is to allow seamless translation between snake_case and camelCase and generate PEP8-compliant code over APIs that support a different casing scheme.\n\n- It introspects a function to obtain the expected argument names\n- It inspects the provided input to find matching candidates\n- It calls the function with the cleaned arguments\n\nIt can also be used to allow for a certain degree of personalization in typically strict contexts such as configuration files and APIs. \n\nTake for example the toml below, where all 3 items are equivalent:\n\n```toml\n[tool.some-plugin]\nenable_features = [\'this\', \'that\']\nenable-features = [\'this\', \'that\']\nenableFeatures = [\'this\', \'that\']\n```\n\nOr maybe in a CLI app, to allow both underscores and dashes:\n\n```shell\n# which one was it?\npoetry install --no-dev\npoetry install --no_dev\n```\n\n\n## dispatch\n\nAn enhanced version of [functools.singledispatch](https://docs.python.org/3.8/library/functools.html#functools.singledispatch):\n\n\n- Adds support for `Type[]` annotations (singledispatch only works on instances)\n- You are no longer limited to the first argument of the method\n- You can target an argument by its name too, regardless of its position\n\n\n## finalizer\n\nA classic and simple try/finally context manager that launches a delegate once a block of code has completed.\n\nA common trick is to "cook" the finalizer arguments through a mutable type such as a list or dict:\n\n```python\nfrom typing import List\nfrom coveo_functools.finalizer import finalizer\n\ndef clean_up(container_names: List[str]) -> None:\n    for _ in container_names:\n        ...\n    \ndef test_spawning_containers() -> None:\n    containers: List[str] = []\n    with finalizer(clean_up, containers):\n        containers.append(\'some-container-1\')\n        containers.append(\'some-container-2\')\n        containers.append(\'some-container-3\')\n```\n\n\n## wait.until()\n\nWaits for a condition to happen. Can be configured with exceptions to ignore.\n\n```python\nfrom coveo_functools import wait\nimport requests\n\ndef _ready() -> bool:\n    return requests.get(\'/ping\').status_code == 200\n\nwait.until(_ready, timeout_s=30, retry_ms=100, handle_exceptions=ConnectionError,\n           failure_message="The service failed to respond in time.")\n```\n\n## wait.Backoff\n\nA customizable class to assist in the creation of backoff retry strategies.\n\n- Customizable growth factor\n- Jitter\n- Backoff progress % (want to fire some preliminary alarms at 50% backoff maybe?)\n- Supports infinite backoff\n- Can be configured to raise after too many attempts\n- Can be configured to raise after a set amount of time\n\ne.g.: Worker loop failure management by catching RetriesExhausted\n\n```python\nfrom coveo_functools.wait import Backoff\n\nbackoff = Backoff()\nwhile my_loop:\n    try:\n        do_stuff()\n    except Exception as exception:\n        try:\n            quit_flag.wait(next(backoff))\n        except backoff.RetriesExhausted:\n            raise exception\n```\n\ne.g.: Worker loop failure management without the nested try/catch:\n\n```python\nfrom coveo_functools.wait import Backoff\n\nbackoff = Backoff()\nwhile my_loop:\n    try:\n        do_stuff()\n    except Exception as exception:\n        wait_time = next(backoff, None)\n        if wait_time is None:\n            raise exception\n        quit_flag.wait(wait_time)\n```\n\ne.g.: You can generate the wait times without creating a Backoff instance, too:\n\n```python\nimport time\nfrom coveo_functools.wait import Backoff\n\nwait_times = list(Backoff.generate_backoff_stages(first_wait, growth, max_backoff))\nfor sleep_time in wait_times:\n    try:\n        do_stuff()\n        break\n    except:\n        time.sleep(sleep_time)\nelse:\n    raise ImSickOfTrying()\n```\n',
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
