# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peano']

package_data = \
{'': ['*']}

install_requires = \
['influxdb-client>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'peano',
    'version': '0.1.3',
    'description': 'Measures performance and reports to InfluxDB',
    'long_description': '# Peano\n\nDecorator for performance measurement\n\n- Measures function calls: TPS and Latency\n- Reports to InfluxDB\n\n## Example\n\n```python\n        peano.init(url, organization, token, bucket)\n\n        @measured()\n        def do_something()\n```\n\n## TODO\n\n- tests\n- async commit to influx\n\n## dev\n\npoetry shell\npoetry update\npytest\npoetry build',
    'author': 'Anton Panchenko',
    'author_email': 'apanchenko@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/apanchenko/peano',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
